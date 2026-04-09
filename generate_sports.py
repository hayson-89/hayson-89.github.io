import anthropic
import datetime
import os
import random
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")

categories = {
    "스포츠뉴스": [
        "손흥민 최근 경기 활약 및 시즌 성적 분석",
        "KBO 리그 최신 순위 및 주요 경기 결과",
        "NBA 플레이오프 주요 경기 하이라이트",
        "국내 축구 K리그 최신 이슈 및 이적 소식",
        "EPL 주요 팀 최신 경기 결과 및 분석",
        "한국 야구 국가대표 최근 소식",
        "한국 배구 V리그 최신 순위 및 이슈",
        "UFC 최신 경기 결과 및 한국 선수 소식",
    ],
    "스포츠정보": [
        "축구 포지션별 역할과 특징 완벽 정리",
        "헬스 초보자를 위한 운동 루틴 가이드",
        "수영 자유형 기초 자세 교정법",
        "골프 입문자를 위한 기초 스윙 가이드",
        "달리기 부상 없이 마라톤 준비하는 방법",
        "배드민턴 서브 잘 넣는 방법",
        "등산 초보자를 위한 장비 선택 가이드",
        "자전거 타기 올바른 자세와 안전 수칙",
    ],
    "스포츠소식": [
        "2026년 국내 생활체육대회 일정 총정리",
        "전국체육대회 참가 신청 방법 안내",
        "지역 스포츠 센터 무료 강습 프로그램 소개",
        "국내 마라톤 대회 일정 및 참가 방법",
        "생활체육 동호회 지원 정책 변경 사항",
        "스포츠 용품 할인 행사 및 이벤트 정보",
    ],
    "스포츠이야기": [
        "처음 축구를 시작했던 날의 기억",
        "동네 야구팀에서 배운 팀워크의 진짜 의미",
        "마라톤 완주 후 느낀 성취감과 교훈",
        "스포츠가 내 삶을 바꾼 이야기",
        "운동을 통해 극복한 슬럼프 이야기",
        "동호회 활동으로 만난 인생 친구들",
        "운동이 정신 건강에 미치는 긍정적 효과",
    ],
}

# 글쓴이 페르소나 (랜덤 선택으로 다양성 확보)
personas = [
    {
        "name": "30대 직장인",
        "style": "퇴근 후 운동하는 직장인의 솔직한 시각으로 쓰되, 가끔 회사 얘기도 섞어가며 자연스럽게",
        "tone": "친근하고 솔직한 직장인 말투, 가끔 피곤하다는 티도 내면서",
    },
    {
        "name": "스포츠 동호회 회원",
        "style": "주말마다 동호회 나가는 아마추어 스포츠 팬의 시각으로, 동호회 경험을 자연스럽게 녹여서",
        "tone": "열정적이지만 전문가인 척하지 않는 아마추어 팬의 말투",
    },
    {
        "name": "스포츠 관람 마니아",
        "style": "경기장에서 직관도 하고 TV로도 보는 열혈 팬의 시각으로, 감정이 풍부하게",
        "tone": "흥분과 실망을 솔직하게 드러내는 팬 말투",
    },
]

thumbnail_styles = {
    "스포츠뉴스": {
        "bg": "linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)",
        "cat_bg": "#e63946",
        "cat_color": "#fff",
    },
    "스포츠정보": {
        "bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)",
        "cat_bg": "#f4a261",
        "cat_color": "#1a1a1a",
    },
    "스포츠소식": {
        "bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)",
        "cat_bg": "#f4a261",
        "cat_color": "#1a1a1a",
    },
    "스포츠이야기": {
        "bg": "linear-gradient(135deg,#0d2137 0%,#1a4a6e 50%,#0077b6 100%)",
        "cat_bg": "#00b4d8",
        "cat_color": "#fff",
    },
}

category_icons = {
    "스포츠뉴스": "⚡",
    "스포츠정보": "📋",
    "스포츠소식": "📢",
    "스포츠이야기": "💬",
}


def make_thumbnail_html(category, title, date_str):
    style = thumbnail_styles.get(category, thumbnail_styles["스포츠뉴스"])
    icon = category_icons.get(category, "🏃")
    short_title = title[:28] + "..." if len(title) > 28 else title

    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:600px;height:400px;overflow:hidden}}
.t{{width:600px;height:400px;background:{bg};position:relative;display:flex;align-items:flex-end;font-family:'Noto Sans KR',sans-serif}}
.o{{position:absolute;inset:0;background:rgba(0,0,0,0.35)}}
.d1{{position:absolute;top:-40px;right:-40px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,0.06)}}
.d2{{position:absolute;bottom:-30px;left:-30px;width:140px;height:140px;border-radius:50%;background:rgba(255,255,255,0.04)}}
.ic{{position:absolute;top:20px;right:20px;z-index:2;width:50px;height:50px;border-radius:50%;background:rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;font-size:26px}}
.c{{position:relative;z-index:2;padding:24px;width:100%}}
.ct{{display:inline-block;font-size:12px;font-weight:700;padding:5px 12px;border-radius:20px;margin-bottom:12px;background:{cat_bg};color:{cat_color};letter-spacing:1px}}
.tt{{font-size:26px;font-weight:700;color:#fff;line-height:1.4;margin:0 0 12px;text-shadow:0 2px 4px rgba(0,0,0,0.5)}}
.m{{display:flex;align-items:center;gap:8px}}
.dt{{font-size:12px;color:rgba(255,255,255,0.7)}}
.dv{{width:1px;height:10px;background:rgba(255,255,255,0.4)}}
.bl{{font-size:12px;color:rgba(255,255,255,0.7)}}
</style></head>
<body>
<div class="t">
  <div class="o"></div><div class="d1"></div><div class="d2"></div>
  <div class="ic">{icon}</div>
  <div class="c">
    <span class="ct">{category}</span>
    <p class="tt">{title}</p>
    <div class="m">
      <span class="dt">{date}</span>
      <span class="dv"></span>
      <span class="bl">생활스포츠 블로그</span>
    </div>
  </div>
</div>
</body></html>""".format(
        bg=style["bg"],
        cat_bg=style["cat_bg"],
        cat_color=style["cat_color"],
        icon=icon,
        category=category,
        title=short_title,
        date=date_str,
    )


def generate_post(category, topic, date_str, persona):
    # 불규칙한 요소들 (AI 티 줄이기)
    random_openers = [
        "오늘 " + topic + " 관련해서 얘기해보려고요.",
        "요즘 " + topic + " 이야기가 많이 나오더라고요.",
        "갑자기 " + topic + " 생각이 나서 글 써봐요.",
        topic + " 관련해서 제 생각 좀 적어볼게요.",
        "친구한테 " + topic + " 얘기 듣고 정리해봤어요.",
    ]

    random_closers = [
        "여러분은 어떻게 생각하세요? 댓글로 얘기 나눠요 :)",
        "저만 이런 생각 드는 건 아니죠? ㅎㅎ 이웃분들 의견도 궁금해요!",
        "다음엔 더 좋은 내용으로 찾아올게요. 공감이나 댓글은 힘이 됩니다!",
        "오늘도 읽어주셔서 감사해요~ 운동 열심히 하는 하루 되세요!",
        "궁금한 점 있으면 댓글 남겨주세요. 아는 범위에서 답해드릴게요!",
    ]

    opener = random.choice(random_openers)
    closer = random.choice(random_closers)

    prompt = """너는 네이버 블로그를 운영하는 """ + persona["name"] + """야.
글쓰기 스타일: """ + persona["style"] + """
말투: """ + persona["tone"] + """

주제: '""" + topic + """' 에 대한 """ + category + """ 글을 써줘.

반드시 지켜야 할 규칙:
1. 첫 문장은 반드시 이걸로 시작해: '""" + opener + """'
2. 마지막 문장은 반드시 이걸로 끝내: '""" + closer + """'
3. AI가 쓴 티가 절대 나면 안 됨. 진짜 사람이 쓴 것처럼.
4. 완벽하게 정제된 문장 쓰지 말 것. 가끔 구어체, 줄임말, 감탄사 사용.
5. 중간에 개인적인 경험이나 느낌 한두 문장 자연스럽게 포함.
6. 소제목은 딱딱한 형식 말고 구어체로 (예: "그래서 어떻게 해야 하냐면요", "이건 진짜 몰랐던 사실").
7. 이모지는 2~3개만, 자연스러운 위치에.
8. 분량은 500~700자.
9. 네이버 SEO 태그 5~7개 마지막에 추가 (형식: #태그1 #태그2 ...).

출력 형식:
제목: (클릭하고 싶은 제목)
---
(본문)
---
태그: #태그1 #태그2 #태그3 #태그4 #태그5"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def send_email(posts_data, date_str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[스포츠 블로그] " + date_str + " 발행 예정 " + str(len(posts_data)) + "편"
    msg["From"] = email_address
    msg["To"] = email_address

    html = """<html><body style="font-family:sans-serif;max-width:700px;margin:0 auto;padding:20px">
<h2 style="color:#333;border-bottom:3px solid #e63946;padding-bottom:10px">
오늘의 스포츠 블로그 글 """ + str(len(posts_data)) + """편 🏃
</h2>
<p style="color:#888;font-size:13px;margin-bottom:24px">
📌 발행 순서: 썸네일 캡처 → 네이버 블로그 글쓰기 → 복붙 → 발행
</p>"""

    for i, post in enumerate(posts_data):
        cat_color = {"스포츠뉴스": "#e63946", "스포츠정보": "#f4a261",
                     "스포츠소식": "#f4a261", "스포츠이야기": "#00b4d8"}.get(post["category"], "#333")

        html += """
<div style="margin:0 0 32px;padding:24px;border:1px solid #eee;border-radius:16px;border-top:4px solid """ + cat_color + """">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
    <span style="background:""" + cat_color + """;color:#fff;font-size:11px;padding:3px 10px;border-radius:20px;font-weight:700">""" + post["category"] + """</span>
    <span style="font-size:12px;color:#999">""" + str(i+1) + """번째 글</span>
  </div>
  <h3 style="color:#222;margin:0 0 16px;font-size:17px;line-height:1.4">""" + post["title"] + """</h3>

  <div style="background:#fffaf0;border-radius:8px;padding:14px;margin-bottom:14px;border:1px solid #ffe0b2">
    <p style="font-size:12px;color:#f57c00;font-weight:700;margin:0 0 8px">📸 썸네일 코드 (브라우저에서 열어서 캡처하세요)</p>
    <textarea style="width:100%;height:70px;font-size:10px;border:1px solid #ddd;border-radius:4px;padding:6px" readonly>""" + post["thumbnail"].replace("<", "&lt;").replace(">", "&gt;") + """</textarea>
  </div>

  <div style="background:#f8f9ff;border-radius:8px;padding:16px;border:1px solid #e8eaf6">
    <p style="font-size:12px;color:#5c6bc0;font-weight:700;margin:0 0 10px">📝 복붙할 본문</p>
    <pre style="white-space:pre-wrap;font-size:14px;color:#333;line-height:1.8;margin:0;font-family:sans-serif">""" + post["content"] + """</pre>
  </div>
</div>"""

    html += """
<div style="background:#f0f7ff;border-radius:12px;padding:16px;font-size:13px;color:#555;line-height:1.8">
<strong>발행 팁 💡</strong><br>
• 썸네일: HTML 코드 → 메모장 저장(.html) → 브라우저 열기 → 캡처<br>
• 하루 2~3편 꾸준히 발행이 네이버 최적화에 유리해요<br>
• 발행 시간은 오전 7~9시, 오후 12~1시, 저녁 7~9시 추천
</div>
</body></html>"""

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)

    print("이메일 전송 완료!")


# 메인 실행
count = int(os.environ.get("POST_COUNT", "2"))
date_str = datetime.date.today().strftime("%Y.%m.%d")

all_cats = list(categories.keys())
selected_cats = []
for i in range(count):
    selected_cats.append(all_cats[i % len(all_cats)])

posts_data = []

for i, category in enumerate(selected_cats):
    persona = random.choice(personas)
    topic = random.choice(categories[category])
    print("[" + str(i+1) + "/" + str(count) + "] " + category + " - " + topic)

    content = generate_post(category, topic, date_str, persona)

    title = topic
    for line in content.split("\n"):
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
            break

    thumbnail = make_thumbnail_html(category, title, date_str)

    posts_data.append({
        "category": category,
        "topic": topic,
        "title": title,
        "content": content,
        "thumbnail": thumbnail,
    })

    print("완료: " + title)
    if i < len(selected_cats) - 1:
        time.sleep(3)

print("이메일 전송 중...")
send_email(posts_data, date_str)
print("모든 작업 완료!")
