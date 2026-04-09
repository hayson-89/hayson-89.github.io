import anthropic
import datetime
import os
import random
import time
import smtplib
import urllib.request
import urllib.parse
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")

# 카테고리별 주제
categories = {
    "스포츠뉴스": [
        "손흥민 최근 경기 활약 및 시즌 성적 분석",
        "KBO 리그 최신 순위 및 주요 경기 결과",
        "NBA 플레이오프 주요 경기 하이라이트",
        "국내 축구 K리그 최신 이슈 및 이적 소식",
        "EPL 주요 팀 최신 경기 결과 및 분석",
        "한국 야구 국가대표 최근 소식",
        "김연아 이후 한국 피겨스케이팅 현황",
        "한국 배구 V리그 최신 순위 및 이슈",
        "UFC 최신 경기 결과 및 한국 선수 소식",
        "테니스 그랜드슬램 최신 소식",
    ],
    "스포츠정보": [
        "축구 포지션별 역할과 특징 완벽 정리",
        "헬스 초보자를 위한 운동 루틴 가이드",
        "수영 자유형 기초 자세 교정법",
        "골프 입문자를 위한 기초 스윙 가이드",
        "달리기 부상 없이 마라톤 준비하는 방법",
        "배드민턴 서브 잘 넣는 방법 완벽 가이드",
        "탁구 기초 기술 마스터하는 방법",
        "등산 초보자를 위한 장비 선택 가이드",
        "자전거 타기 올바른 자세와 안전 수칙",
        "요가 초보자를 위한 기초 동작 모음",
    ],
    "스포츠소식": [
        "2026년 국내 생활체육대회 일정 총정리",
        "전국체육대회 참가 신청 방법 안내",
        "지역 스포츠 센터 무료 강습 프로그램 소개",
        "국민체육진흥공단 스포츠 지원 사업 안내",
        "학교 스포츠 클럽 활성화 최신 소식",
        "2026 아시안게임 한국 대표팀 선발 소식",
        "국내 마라톤 대회 일정 및 참가 방법",
        "생활체육 동호회 지원 정책 변경 사항",
        "스포츠 용품 할인 행사 및 이벤트 정보",
        "국내 스포츠 시설 개방 및 이용 안내",
    ],
    "스포츠이야기": [
        "내가 처음 축구를 시작했던 날의 기억",
        "동네 야구팀에서 배운 팀워크의 진짜 의미",
        "마라톤 완주 후 느낀 성취감과 교훈",
        "스포츠가 내 삶을 바꾼 이야기",
        "아버지와 함께한 캐치볼의 추억",
        "운동을 통해 극복한 슬럼프 이야기",
        "동호회 활동으로 만난 인생 친구들",
        "스포츠 관람의 묘미 직관 vs 중계 비교",
        "운동이 정신 건강에 미치는 긍정적 효과",
        "나만의 운동 루틴을 만들기까지의 여정",
    ],
}

# 카테고리별 썸네일 스타일
thumbnail_styles = {
    "스포츠뉴스": {
        "bg": "linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)",
        "cat_bg": "#e63946",
        "cat_color": "#fff",
        "icon_color": "#e63946",
    },
    "스포츠정보": {
        "bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)",
        "cat_bg": "#f4a261",
        "cat_color": "#1a1a1a",
        "icon_color": "#f4a261",
    },
    "스포츠소식": {
        "bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)",
        "cat_bg": "#f4a261",
        "cat_color": "#1a1a1a",
        "icon_color": "#f4a261",
    },
    "스포츠이야기": {
        "bg": "linear-gradient(135deg,#0d2137 0%,#1a4a6e 50%,#0077b6 100%)",
        "cat_bg": "#00b4d8",
        "cat_color": "#fff",
        "icon_color": "#00b4d8",
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
<html>
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:600px;height:400px;overflow:hidden}}
.thumb{{width:600px;height:400px;background:{bg};position:relative;display:flex;align-items:flex-end;font-family:'Noto Sans KR',sans-serif}}
.overlay{{position:absolute;inset:0;background:rgba(0,0,0,0.35)}}
.deco1{{position:absolute;top:-40px;right:-40px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,0.06)}}
.deco2{{position:absolute;bottom:-30px;left:-30px;width:140px;height:140px;border-radius:50%;background:rgba(255,255,255,0.04)}}
.icon{{position:absolute;top:20px;right:20px;z-index:2;width:50px;height:50px;border-radius:50%;background:rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;font-size:26px}}
.content{{position:relative;z-index:2;padding:24px;width:100%}}
.cat{{display:inline-block;font-size:12px;font-weight:700;padding:5px 12px;border-radius:20px;margin-bottom:12px;background:{cat_bg};color:{cat_color};letter-spacing:1px}}
.title{{font-size:26px;font-weight:700;color:#fff;line-height:1.4;margin:0 0 12px;text-shadow:0 2px 4px rgba(0,0,0,0.5)}}
.meta{{display:flex;align-items:center;gap:8px}}
.date{{font-size:12px;color:rgba(255,255,255,0.7)}}
.div{{width:1px;height:10px;background:rgba(255,255,255,0.4)}}
.blog{{font-size:12px;color:rgba(255,255,255,0.7)}}
</style>
</head>
<body>
<div class="thumb">
  <div class="overlay"></div>
  <div class="deco1"></div>
  <div class="deco2"></div>
  <div class="icon">{icon}</div>
  <div class="content">
    <span class="cat">{category}</span>
    <p class="title">{title}</p>
    <div class="meta">
      <span class="date">{date}</span>
      <span class="div"></span>
      <span class="blog">생활스포츠 블로그</span>
    </div>
  </div>
</div>
</body>
</html>""".format(
        bg=style["bg"],
        cat_bg=style["cat_bg"],
        cat_color=style["cat_color"],
        icon=icon,
        category=category,
        title=short_title,
        date=date_str,
    )


def generate_post(category, topic, date_str):
    prompt = "다음 주제로 네이버 블로그용 한국어 스포츠 글을 작성해줘: \"" + topic + "\"\n\n"
    prompt += "카테고리: " + category + "\n\n"
    prompt += "아래 형식으로 작성해줘:\n\n"
    prompt += "제목: (매력적인 제목)\n\n"
    prompt += "태그: (관련 태그 5~8개, 쉼표로 구분)\n\n"
    prompt += "본문:\n(내용)\n\n"
    prompt += "규칙:\n"
    prompt += "- 본문 600~800자\n"
    prompt += "- 소제목 2~3개 포함\n"
    prompt += "- 네이버 블로그 특성상 친근하고 읽기 쉬운 문체\n"
    prompt += "- 이모지 2~3개 자연스럽게 포함\n"
    prompt += "- 마지막에 독자 참여 유도 문구 포함\n"
    prompt += "- SEO를 위해 핵심 키워드 자연스럽게 3~4회 반복"

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def send_email(posts_data, date_str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[스포츠 블로그] " + date_str + " 발행 예정 글 " + str(len(posts_data)) + "편"
    msg["From"] = email_address
    msg["To"] = email_address

    html_content = """
<html><body style="font-family:sans-serif;max-width:700px;margin:0 auto;padding:20px">
<h2 style="color:#333;border-bottom:2px solid #e63946;padding-bottom:10px">
오늘의 스포츠 블로그 글 """ + str(len(posts_data)) + """편
</h2>
<p style="color:#666;font-size:14px">아래 글을 네이버 블로그에 복붙하세요!</p>
"""

    for i, post in enumerate(posts_data):
        html_content += """
<div style="margin:30px 0;padding:24px;border:1px solid #eee;border-radius:12px">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <span style="background:#e63946;color:#fff;font-size:12px;padding:4px 10px;border-radius:20px;font-weight:700">
      """ + post["category"] + """
    </span>
    <span style="font-size:13px;color:#999">글 """ + str(i+1) + """</span>
  </div>

  <h3 style="color:#222;margin:0 0 12px;font-size:18px">""" + post["title"] + """</h3>

  <div style="background:#f8f8f8;border-radius:8px;padding:16px;margin-bottom:16px">
    <p style="font-size:12px;color:#999;margin:0 0 6px">썸네일 HTML (캡처 후 사용)</p>
    <details>
      <summary style="font-size:13px;color:#666;cursor:pointer">썸네일 코드 보기</summary>
      <textarea style="width:100%;height:80px;font-size:11px;margin-top:8px">""" + post["thumbnail"].replace("<", "&lt;").replace(">", "&gt;") + """</textarea>
    </details>
  </div>

  <div style="background:#fff9f9;border-left:4px solid #e63946;padding:16px;border-radius:0 8px 8px 0">
    <p style="font-size:12px;color:#999;margin:0 0 8px">복사할 본문</p>
    <pre style="white-space:pre-wrap;font-size:14px;color:#333;line-height:1.7;margin:0">""" + post["content"] + """</pre>
  </div>
</div>
"""

    html_content += """
<div style="background:#f0f7ff;border-radius:12px;padding:16px;margin-top:20px">
  <p style="font-size:13px;color:#555;margin:0">
    📌 네이버 블로그 발행 순서<br>
    1. 썸네일 HTML을 브라우저에서 열어 캡처<br>
    2. 네이버 블로그 글쓰기 → 대표 이미지로 썸네일 업로드<br>
    3. 제목 + 태그 + 본문 복붙<br>
    4. 발행!
  </p>
</div>
</body></html>
"""

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)

    print("이메일 전송 완료: " + email_address)


# 메인 실행
count = int(os.environ.get("POST_COUNT", "2"))
date_str = datetime.date.today().strftime("%Y.%m.%d")

# 카테고리 순환 선택
all_cats = list(categories.keys())
selected_cats = []
for i in range(count):
    selected_cats.append(all_cats[i % len(all_cats)])

posts_data = []

for i, category in enumerate(selected_cats):
    topic = random.choice(categories[category])
    print("[" + str(i+1) + "/" + str(count) + "] 생성 중: " + category + " - " + topic)

    content = generate_post(category, topic, date_str)

    # 제목 추출
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
        time.sleep(2)

# 이메일 전송
print("이메일 전송 중...")
send_email(posts_data, date_str)
print("모든 작업 완료!")
