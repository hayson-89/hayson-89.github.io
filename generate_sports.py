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
from email.mime.image import MIMEImage
from playwright.sync_api import sync_playwright

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")

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

# 주제별 Unsplash 검색 키워드 (정확한 매핑)
topic_keywords = {
    # 스포츠뉴스
    "손흥민": ["son heungmin football", "tottenham soccer", "korean soccer player"],
    "KBO": ["baseball korea", "baseball stadium", "baseball game"],
    "NBA": ["basketball nba", "basketball game", "basketball player dunking"],
    "K리그": ["korean football league", "soccer match korea", "football stadium korea"],
    "EPL": ["premier league football", "english soccer", "football match stadium"],
    "야구 국가대표": ["korea baseball team", "baseball pitcher", "baseball national team"],
    "배구": ["volleyball game", "volleyball player", "volleyball match"],
    "UFC": ["mma fighting", "ufc fighter", "martial arts combat"],
    # 스포츠정보
    "축구 포지션": ["soccer tactics", "football formation", "soccer player position"],
    "헬스": ["gym workout", "fitness training", "weight lifting gym"],
    "수영": ["swimming pool", "freestyle swimming", "swimmer underwater"],
    "골프": ["golf swing", "golf course", "golfer playing"],
    "달리기": ["running marathon", "runner road", "jogging outdoor"],
    "배드민턴": ["badminton court", "badminton player", "badminton smash"],
    "등산": ["hiking mountain", "mountain trail", "hiker trekking"],
    "자전거": ["cycling road", "bicycle rider", "mountain biking"],
    # 스포츠소식
    "생활체육대회": ["sports community event", "amateur sports competition", "sports festival"],
    "전국체육대회": ["national sports games", "athletics competition", "sports tournament"],
    "스포츠 센터": ["sports center indoor", "fitness center", "sports facility"],
    "마라톤 대회": ["marathon race", "marathon runners road", "running competition"],
    "동호회": ["sports club team", "amateur sports team", "community sports"],
    "스포츠 용품": ["sports equipment store", "athletic gear", "sports shoes"],
    # 스포츠이야기
    "축구를 시작": ["kids playing soccer", "youth football", "soccer beginners"],
    "야구팀": ["baseball team", "baseball players dugout", "amateur baseball"],
    "마라톤 완주": ["marathon finish line", "runner crossing finish", "marathon achievement"],
    "스포츠가 내 삶": ["sports lifestyle", "athlete motivation", "sports inspiration"],
    "슬럼프": ["athlete determination", "sports comeback", "perseverance sports"],
    "동호회 활동": ["sports friends team", "group sports activity", "sports community"],
    "정신 건강": ["meditation sports", "wellness exercise", "mental health fitness"],
}

# 기본 폴백 키워드 (매핑 못 찾을 때)
default_keywords = {
    "스포츠뉴스": ["sports news", "athlete competition", "sports stadium"],
    "스포츠정보": ["sports training", "fitness workout", "athlete exercise"],
    "스포츠소식": ["sports event", "sports community", "athletic competition"],
    "스포츠이야기": ["sports lifestyle", "team sports", "outdoor sports"],
}

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
    "스포츠뉴스": {"bg": "linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)", "cat_bg": "#e63946", "cat_color": "#fff"},
    "스포츠정보": {"bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)", "cat_bg": "#f4a261", "cat_color": "#1a1a1a"},
    "스포츠소식": {"bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)", "cat_bg": "#f4a261", "cat_color": "#1a1a1a"},
    "스포츠이야기": {"bg": "linear-gradient(135deg,#0d2137 0%,#1a4a6e 50%,#0077b6 100%)", "cat_bg": "#00b4d8", "cat_color": "#fff"},
}

category_icons = {
    "스포츠뉴스": "⚡",
    "스포츠정보": "📋",
    "스포츠소식": "📢",
    "스포츠이야기": "💬",
}


def get_topic_keywords(topic, category):
    """주제에 맞는 정확한 키워드 반환"""
    for key, keywords in topic_keywords.items():
        if key in topic:
            return keywords
    return default_keywords.get(category, ["sports athlete"])


def get_unsplash_images(topic, category, count=3):
    if not unsplash_key:
        print("UNSPLASH_ACCESS_KEY 없음")
        return []

    keywords = get_topic_keywords(topic, category)
    images = []

    for i in range(count):
        try:
            query = keywords[i % len(keywords)]
            print("이미지 검색: " + query)
            encoded = urllib.parse.quote(query)
            url = ("https://api.unsplash.com/photos/random?query=" + encoded +
                   "&orientation=landscape&client_id=" + unsplash_key)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode())
                img_url = data["urls"]["regular"]
                print("이미지 다운로드: " + img_url[:50] + "...")
                img_req = urllib.request.Request(
                    img_url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(img_req, timeout=20) as img_res:
                    img_bytes = img_res.read()
                print("이미지" + str(i+1) + " 완료 (" + str(len(img_bytes)) + " bytes)")
                images.append({
                    "bytes": img_bytes,
                    "photographer": data["user"]["name"],
                    "link": data["links"]["html"],
                    "query": query,
                })
            time.sleep(1)
        except Exception as e:
            print("이미지" + str(i+1) + " 실패: " + str(e))

    return images


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
        bg=style["bg"], cat_bg=style["cat_bg"], cat_color=style["cat_color"],
        icon=icon, category=category, title=short_title, date=date_str,
    )


def html_to_png(html_content):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 600, "height": 400})
        page.set_content(html_content)
        page.wait_for_timeout(1500)
        img_bytes = page.screenshot(clip={"x": 0, "y": 0, "width": 600, "height": 400})
        browser.close()
        return img_bytes


def generate_post(category, topic, date_str, persona, image_count):
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

    img1_ph = "\n\n▶ [이미지1 여기에 삽입]\n\n" if image_count >= 1 else ""
    img2_ph = "\n\n▶ [이미지2 여기에 삽입]\n\n" if image_count >= 2 else ""
    img3_ph = "\n\n▶ [이미지3 여기에 삽입]\n\n" if image_count >= 3 else ""

    prompt = ("너는 네이버 블로그를 운영하는 " + persona["name"] + "야.\n"
              "글쓰기 스타일: " + persona["style"] + "\n"
              "말투: " + persona["tone"] + "\n\n"
              "주제: '" + topic + "' 에 대한 " + category + " 글을 써줘.\n\n"
              "아래 구조로 작성해줘:\n\n"
              "제목: (클릭하고 싶은 제목)\n"
              "---\n"
              "[도입부 - 3~4문장]\n"
              "첫 문장 반드시: '" + opener + "'\n"
              + img1_ph +
              "[섹션1 소제목 (구어체로)]\n"
              "(내용 400~500자)\n"
              + img2_ph +
              "[섹션2 소제목 (구어체로)]\n"
              "(내용 400~500자, 개인 경험 포함)\n"
              + img3_ph +
              "[섹션3 소제목 (구어체로)]\n"
              "(내용 400~500자, 실용적인 팁)\n\n"
              "[마무리 2~3문장]\n"
              "마지막 문장 반드시: '" + closer + "'\n"
              "---\n"
              "태그: #태그1 #태그2 #태그3 #태그4 #태그5 #태그6 #태그7\n\n"
              "규칙:\n"
              "- 총 글자 수 1500~2000자\n"
              "- [이미지N 여기에 삽입] 표시 반드시 그대로 유지\n"
              "- AI 티 절대 내지 말 것\n"
              "- 구어체, 줄임말, 감탄사 자유롭게\n"
              "- 소제목은 구어체로\n"
              "- 이모지 4~6개 자연스럽게")

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def send_email(posts_data, date_str):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = "[스포츠 블로그] " + date_str + " 발행 예정 " + str(len(posts_data)) + "편"
    msg["From"] = email_address
    msg["To"] = email_address

    cat_colors = {
        "스포츠뉴스": "#e63946",
        "스포츠정보": "#f4a261",
        "스포츠소식": "#f4a261",
        "스포츠이야기": "#00b4d8",
    }

    html = ("<html><body style='font-family:sans-serif;max-width:700px;margin:0 auto;padding:20px'>"
            "<h2 style='color:#333;border-bottom:3px solid #e63946;padding-bottom:10px'>"
            "오늘의 스포츠 블로그 글 " + str(len(posts_data)) + "편 🏃</h2>"
            "<div style='background:#fff9e6;border-radius:12px;padding:16px;margin-bottom:24px;"
            "border:1px solid #ffe0b2;font-size:13px;color:#555;line-height:1.8'>"
            "<strong>📌 네이버 블로그 발행 순서</strong><br>"
            "1. 썸네일 PNG → 네이버 블로그 대표 이미지 업로드<br>"
            "2. 제목 복붙<br>"
            "3. 본문 복붙 후 ▶ [이미지N 여기에 삽입] 위치에 첨부 이미지 순서대로 업로드<br>"
            "4. 태그 입력 → 발행!</div>")

    img_attach_index = 0

    for i, post in enumerate(posts_data):
        color = cat_colors.get(post["category"], "#333")
        thumb_cid = "thumb_" + str(i)

        html += ("<div style='margin:0 0 32px;padding:24px;border:1px solid #eee;"
                 "border-radius:16px;border-top:4px solid " + color + "'>"
                 "<div style='display:flex;align-items:center;gap:8px;margin-bottom:14px'>"
                 "<span style='background:" + color + ";color:#fff;font-size:11px;"
                 "padding:3px 10px;border-radius:20px;font-weight:700'>" + post["category"] + "</span>"
                 "<span style='font-size:12px;color:#999'>" + str(i+1) + "번째 글</span></div>"
                 "<h3 style='color:#222;margin:0 0 16px;font-size:17px'>" + post["title"] + "</h3>"
                 "<div style='margin-bottom:16px;background:#f5f5f5;border-radius:8px;padding:12px'>"
                 "<p style='font-size:12px;color:#f57c00;font-weight:700;margin:0 0 8px'>📸 썸네일 (대표 이미지로 업로드)</p>"
                 "<img src='cid:" + thumb_cid + "' style='width:280px;border-radius:8px'></div>")

        if post["images"]:
            html += ("<div style='margin-bottom:16px;background:#f0fff4;border-radius:8px;padding:12px;"
                     "border:1px solid #c8e6c9'>"
                     "<p style='font-size:12px;color:#388e3c;font-weight:700;margin:0 0 10px'>"
                     "🖼 본문 이미지 " + str(len(post["images"])) + "장 — ▶ [이미지N] 위치에 순서대로 업로드</p>"
                     "<div style='display:flex;gap:8px;flex-wrap:wrap'>")

            for j, img in enumerate(post["images"]):
                img_cid = "img_" + str(img_attach_index)
                html += ("<div style='text-align:center'>"
                         "<img src='cid:" + img_cid + "' style='width:150px;border-radius:6px'>"
                         "<p style='font-size:10px;color:#999;margin:4px 0 0'>"
                         "이미지" + str(j+1) + " (" + img["query"] + ")</p></div>")
                img_attach_index += 1

            html += "</div></div>"

        html += ("<div style='background:#f8f9ff;border-radius:8px;padding:16px;border:1px solid #e8eaf6'>"
                 "<p style='font-size:12px;color:#5c6bc0;font-weight:700;margin:0 0 10px'>📝 복붙할 본문</p>"
                 "<pre style='white-space:pre-wrap;font-size:14px;color:#333;line-height:1.8;"
                 "margin:0;font-family:sans-serif'>" + post["content"] + "</pre></div></div>")

    html += "</body></html>"
    msg.attach(MIMEText(html, "html"))

    for i, post in enumerate(posts_data):
        img = MIMEImage(post["thumbnail_png"], _subtype="png")
        img.add_header("Content-ID", "<thumb_" + str(i) + ">")
        img.add_header("Content-Disposition", "attachment",
                       filename="썸네일_" + str(i+1) + "_" + post["category"] + ".png")
        msg.attach(img)

    total_idx = 0
    for i, post in enumerate(posts_data):
        for j, image in enumerate(post["images"]):
            img = MIMEImage(image["bytes"], _subtype="jpeg")
            img.add_header("Content-ID", "<img_" + str(total_idx) + ">")
            img.add_header("Content-Disposition", "attachment",
                           filename="본문이미지_" + str(i+1) + "_" + str(j+1) + ".jpg")
            msg.attach(img)
            total_idx += 1

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)

    print("이메일 전송 완료!")


# 메인 실행
count = int(os.environ.get("POST_COUNT", "2"))
date_str = datetime.date.today().strftime("%Y.%m.%d")

all_cats = list(categories.keys())
selected_cats = [all_cats[i % len(all_cats)] for i in range(count)]

posts_data = []

for i, category in enumerate(selected_cats):
    persona = random.choice(personas)
    topic = random.choice(categories[category])
    print("[" + str(i+1) + "/" + str(count) + "] " + category + " - " + topic)

    print("이미지 다운로드 중...")
    images = get_unsplash_images(topic, category, count=3)
    print("이미지 " + str(len(images)) + "장 준비 완료")

    content = generate_post(category, topic, date_str, persona, len(images))

    title = topic
    for line in content.split("\n"):
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
            break

    print("썸네일 PNG 변환 중...")
    thumbnail_html = make_thumbnail_html(category, title, date_str)
    thumbnail_png = html_to_png(thumbnail_html)

    posts_data.append({
        "category": category,
        "topic": topic,
        "title": title,
        "content": content,
        "thumbnail_png": thumbnail_png,
        "images": images,
    })

    print("완료: " + title)
    if i < len(selected_cats) - 1:
        time.sleep(3)

print("이메일 전송 중...")
send_email(posts_data, date_str)
print("모든 작업 완료!")import anthropic
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
from email.mime.image import MIMEImage
from playwright.sync_api import sync_playwright

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")

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

unsplash_keywords = {
    "스포츠뉴스": ["soccer match", "football stadium", "sports news", "athlete competition"],
    "스포츠정보": ["fitness workout", "sports training", "exercise gym", "athlete training"],
    "스포츠소식": ["sports event", "marathon running", "sports community", "athletic competition"],
    "스포츠이야기": ["team sports", "outdoor sports", "friends playing sports", "sport lifestyle"],
}

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
    "스포츠뉴스": {"bg": "linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)", "cat_bg": "#e63946", "cat_color": "#fff"},
    "스포츠정보": {"bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)", "cat_bg": "#f4a261", "cat_color": "#1a1a1a"},
    "스포츠소식": {"bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)", "cat_bg": "#f4a261", "cat_color": "#1a1a1a"},
    "스포츠이야기": {"bg": "linear-gradient(135deg,#0d2137 0%,#1a4a6e 50%,#0077b6 100%)", "cat_bg": "#00b4d8", "cat_color": "#fff"},
}

category_icons = {
    "스포츠뉴스": "⚡",
    "스포츠정보": "📋",
    "스포츠소식": "📢",
    "스포츠이야기": "💬",
}


def get_unsplash_images(category, count=3):
    if not unsplash_key:
        return []
    keywords = unsplash_keywords.get(category, ["sports"])
    images = []
    used_queries = []
    for i in range(count):
        try:
            query = random.choice([k for k in keywords if k not in used_queries] or keywords)
            used_queries.append(query)
            encoded = urllib.parse.quote(query)
            url = ("https://api.unsplash.com/photos/random?query=" + encoded +
                   "&orientation=landscape&client_id=" + unsplash_key)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read().decode())
                # 이미지 바이트 다운로드
                img_url = data["urls"]["regular"]
                img_req = urllib.request.Request(img_url)
                with urllib.request.urlopen(img_req, timeout=15) as img_res:
                    img_bytes = img_res.read()
                images.append({
                    "bytes": img_bytes,
                    "photographer": data["user"]["name"],
                    "link": data["links"]["html"],
                })
            time.sleep(0.5)
        except Exception as e:
            print("이미지 가져오기 실패: " + str(e))
    return images


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
        bg=style["bg"], cat_bg=style["cat_bg"], cat_color=style["cat_color"],
        icon=icon, category=category, title=short_title, date=date_str,
    )


def html_to_png(html_content):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 600, "height": 400})
        page.set_content(html_content)
        page.wait_for_timeout(1500)
        img_bytes = page.screenshot(clip={"x": 0, "y": 0, "width": 600, "height": 400})
        browser.close()
        return img_bytes


def generate_post(category, topic, date_str, persona, image_count):
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

    # 이미지 위치 표시 (네이버 블로그용)
    img_placeholder = ""
    for j in range(image_count):
        img_placeholder += "\n\n▶ [이미지" + str(j+1) + " 여기에 삽입]\n\n"

    img1_ph = "\n\n▶ [이미지1 여기에 삽입]\n\n" if image_count >= 1 else ""
    img2_ph = "\n\n▶ [이미지2 여기에 삽입]\n\n" if image_count >= 2 else ""
    img3_ph = "\n\n▶ [이미지3 여기에 삽입]\n\n" if image_count >= 3 else ""

    prompt = ("너는 네이버 블로그를 운영하는 " + persona["name"] + "야.\n"
              "글쓰기 스타일: " + persona["style"] + "\n"
              "말투: " + persona["tone"] + "\n\n"
              "주제: '" + topic + "' 에 대한 " + category + " 글을 써줘.\n\n"
              "아래 구조로 작성해줘:\n\n"
              "제목: (클릭하고 싶은 제목)\n"
              "---\n"
              "[도입부 - 3~4문장]\n"
              "첫 문장 반드시: '" + opener + "'\n"
              + img1_ph +
              "[섹션1 소제목 (구어체로)]\n"
              "(내용 400~500자)\n"
              + img2_ph +
              "[섹션2 소제목 (구어체로)]\n"
              "(내용 400~500자, 개인 경험 포함)\n"
              + img3_ph +
              "[섹션3 소제목 (구어체로)]\n"
              "(내용 400~500자, 실용적인 팁)\n\n"
              "[마무리 2~3문장]\n"
              "마지막 문장 반드시: '" + closer + "'\n"
              "---\n"
              "태그: #태그1 #태그2 #태그3 #태그4 #태그5 #태그6 #태그7\n\n"
              "규칙:\n"
              "- 총 글자 수 1500~2000자\n"
              "- [이미지N 여기에 삽입] 표시는 반드시 그대로 유지할 것\n"
              "- AI 티 절대 내지 말 것\n"
              "- 구어체, 줄임말, 감탄사 자유롭게\n"
              "- 소제목은 구어체로\n"
              "- 이모지 4~6개 자연스럽게")

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def send_email(posts_data, date_str):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = "[스포츠 블로그] " + date_str + " 발행 예정 " + str(len(posts_data)) + "편"
    msg["From"] = email_address
    msg["To"] = email_address

    cat_colors = {
        "스포츠뉴스": "#e63946",
        "스포츠정보": "#f4a261",
        "스포츠소식": "#f4a261",
        "스포츠이야기": "#00b4d8",
    }

    html = ("<html><body style='font-family:sans-serif;max-width:700px;margin:0 auto;padding:20px'>"
            "<h2 style='color:#333;border-bottom:3px solid #e63946;padding-bottom:10px'>"
            "오늘의 스포츠 블로그 글 " + str(len(posts_data)) + "편 🏃</h2>"
            "<div style='background:#fff9e6;border-radius:12px;padding:16px;margin-bottom:24px;"
            "border:1px solid #ffe0b2;font-size:13px;color:#555;line-height:1.8'>"
            "<strong>📌 네이버 블로그 발행 순서</strong><br>"
            "1. 썸네일 PNG → 네이버 블로그 대표 이미지로 업로드<br>"
            "2. 제목 복붙<br>"
            "3. 본문 복붙 (▶ [이미지N 여기에 삽입] 위치에 첨부 이미지 업로드)<br>"
            "4. 태그 입력 후 발행!</div>")

    img_attach_index = 0

    for i, post in enumerate(posts_data):
        color = cat_colors.get(post["category"], "#333")
        thumb_cid = "thumb_" + str(i)

        html += ("<div style='margin:0 0 32px;padding:24px;border:1px solid #eee;"
                 "border-radius:16px;border-top:4px solid " + color + "'>"
                 "<div style='display:flex;align-items:center;gap:8px;margin-bottom:14px'>"
                 "<span style='background:" + color + ";color:#fff;font-size:11px;"
                 "padding:3px 10px;border-radius:20px;font-weight:700'>" + post["category"] + "</span>"
                 "<span style='font-size:12px;color:#999'>" + str(i+1) + "번째 글</span></div>"
                 "<h3 style='color:#222;margin:0 0 16px;font-size:17px'>" + post["title"] + "</h3>"

                 # 썸네일
                 "<div style='margin-bottom:16px;background:#f5f5f5;border-radius:8px;padding:12px'>"
                 "<p style='font-size:12px;color:#f57c00;font-weight:700;margin:0 0 8px'>📸 썸네일 (대표 이미지로 업로드)</p>"
                 "<img src='cid:" + thumb_cid + "' style='width:280px;border-radius:8px'></div>"

                 # 본문 이미지
                 "<div style='margin-bottom:16px;background:#f0fff4;border-radius:8px;padding:12px;"
                 "border:1px solid #c8e6c9'>"
                 "<p style='font-size:12px;color:#388e3c;font-weight:700;margin:0 0 10px'>"
                 "🖼 본문 삽입 이미지 (" + str(len(post["images"])) + "장) — ▶ [이미지N] 위치에 순서대로 업로드</p>"
                 "<div style='display:flex;gap:8px;flex-wrap:wrap'>")

        for j, img in enumerate(post["images"]):
            img_cid = "img_" + str(img_attach_index)
            html += ("<div style='text-align:center'>"
                     "<img src='cid:" + img_cid + "' style='width:150px;border-radius:6px'>"
                     "<p style='font-size:10px;color:#999;margin:4px 0 0'>이미지" + str(j+1) + "</p></div>")
            img_attach_index += 1

        html += ("</div></div>"

                 # 본문
                 "<div style='background:#f8f9ff;border-radius:8px;padding:16px;border:1px solid #e8eaf6'>"
                 "<p style='font-size:12px;color:#5c6bc0;font-weight:700;margin:0 0 10px'>📝 복붙할 본문</p>"
                 "<pre style='white-space:pre-wrap;font-size:14px;color:#333;line-height:1.8;"
                 "margin:0;font-family:sans-serif'>" + post["content"] + "</pre></div></div>")

    html += "</body></html>"
    msg.attach(MIMEText(html, "html"))

    # 썸네일 PNG 첨부
    for i, post in enumerate(posts_data):
        img = MIMEImage(post["thumbnail_png"], _subtype="png")
        img.add_header("Content-ID", "<thumb_" + str(i) + ">")
        img.add_header("Content-Disposition", "attachment",
                       filename="썸네일_" + str(i+1) + "_" + post["category"] + ".png")
        msg.attach(img)

    # 본문 이미지 첨부
    total_idx = 0
    for i, post in enumerate(posts_data):
        for j, image in enumerate(post["images"]):
            img = MIMEImage(image["bytes"], _subtype="jpeg")
            img.add_header("Content-ID", "<img_" + str(total_idx) + ">")
            img.add_header("Content-Disposition", "attachment",
                           filename="본문이미지_" + str(i+1) + "_" + str(j+1) + ".jpg")
            msg.attach(img)
            total_idx += 1

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)

    print("이메일 전송 완료!")


# 메인 실행
count = int(os.environ.get("POST_COUNT", "2"))
date_str = datetime.date.today().strftime("%Y.%m.%d")

all_cats = list(categories.keys())
selected_cats = [all_cats[i % len(all_cats)] for i in range(count)]

posts_data = []

for i, category in enumerate(selected_cats):
    persona = random.choice(personas)
    topic = random.choice(categories[category])
    print("[" + str(i+1) + "/" + str(count) + "] " + category + " - " + topic)

    print("이미지 다운로드 중...")
    images = get_unsplash_images(category, count=3)
    print("이미지 " + str(len(images)) + "장 준비 완료")

    content = generate_post(category, topic, date_str, persona, len(images))

    title = topic
    for line in content.split("\n"):
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
            break

    print("썸네일 PNG 변환 중...")
    thumbnail_html = make_thumbnail_html(category, title, date_str)
    thumbnail_png = html_to_png(thumbnail_html)

    posts_data.append({
        "category": category,
        "topic": topic,
        "title": title,
        "content": content,
        "thumbnail_png": thumbnail_png,
        "images": images,
    })

    print("완료: " + title)
    if i < len(selected_cats) - 1:
        time.sleep(3)

print("이메일 전송 중...")
send_email(posts_data, date_str)
print("모든 작업 완료!")
