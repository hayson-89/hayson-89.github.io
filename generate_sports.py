import anthropic
import datetime
import os
import random
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from sports_config import CATEGORIES, PERSONAS
from sports_utils import get_unsplash_images, make_thumbnail_html, html_to_png

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")


def generate_post(category, topic, date_str, persona, image_count):
    openers = [
        "오늘 " + topic + " 관련해서 얘기해보려고요.",
        "요즘 " + topic + " 이야기가 많이 나오더라고요.",
        "갑자기 " + topic + " 생각이 나서 글 써봐요.",
        topic + " 관련해서 제 생각 좀 적어볼게요.",
        "친구한테 " + topic + " 얘기 듣고 정리해봤어요.",
    ]
    closers = [
        "여러분은 어떻게 생각하세요? 댓글로 얘기 나눠요 :)",
        "저만 이런 생각 드는 건 아니죠? ㅎㅎ 이웃분들 의견도 궁금해요!",
        "다음엔 더 좋은 내용으로 찾아올게요. 공감이나 댓글은 힘이 됩니다!",
        "오늘도 읽어주셔서 감사해요~ 운동 열심히 하는 하루 되세요!",
        "궁금한 점 있으면 댓글 남겨주세요. 아는 범위에서 답해드릴게요!",
    ]
    opener = random.choice(openers)
    closer = random.choice(closers)

    img1 = "\n\n▶ [이미지1 여기에 삽입]\n\n" if image_count >= 1 else ""
    img2 = "\n\n▶ [이미지2 여기에 삽입]\n\n" if image_count >= 2 else ""
    img3 = "\n\n▶ [이미지3 여기에 삽입]\n\n" if image_count >= 3 else ""

    prompt = (
        "너는 네이버 블로그를 운영하는 " + persona["name"] + "야.\n"
        "스타일: " + persona["style"] + "\n"
        "말투: " + persona["tone"] + "\n\n"
        "주제: '" + topic + "' 에 대한 " + category + " 글을 써줘.\n\n"
        "구조:\n"
        "제목: (클릭하고 싶은 제목)\n"
        "---\n"
        "[도입부 3~4문장, 첫 문장: '" + opener + "']\n"
        + img1 +
        "[섹션1 소제목]\n(내용 400~500자)\n"
        + img2 +
        "[섹션2 소제목]\n(내용 400~500자, 개인 경험 포함)\n"
        + img3 +
        "[섹션3 소제목]\n(내용 400~500자, 실용적인 팁)\n\n"
        "[마무리, 마지막 문장: '" + closer + "']\n"
        "---\n"
        "태그: #태그1 #태그2 #태그3 #태그4 #태그5 #태그6 #태그7\n\n"
        "규칙:\n"
        "- 총 1500~2000자\n"
        "- [이미지N 여기에 삽입] 반드시 그대로 유지\n"
        "- AI 티 절대 내지 말 것\n"
        "- 구어체, 줄임말, 감탄사 자유롭게\n"
        "- 소제목은 구어체로\n"
        "- 이모지 4~6개"
    )

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


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

    html = (
        "<html><body style='font-family:sans-serif;max-width:700px;margin:0 auto;padding:20px'>"
        "<h2 style='color:#333;border-bottom:3px solid #e63946;padding-bottom:10px'>"
        "오늘의 스포츠 블로그 글 " + str(len(posts_data)) + "편 🏃</h2>"
        "<div style='background:#fff9e6;border-radius:12px;padding:16px;margin-bottom:24px;"
        "border:1px solid #ffe0b2;font-size:13px;color:#555;line-height:1.8'>"
        "<strong>📌 발행 순서</strong><br>"
        "1. 썸네일 PNG → 네이버 대표 이미지 업로드<br>"
        "2. 제목 복붙<br>"
        "3. 본문 복붙 후 ▶ [이미지N] 위치에 첨부 이미지 순서대로 업로드<br>"
        "4. 태그 입력 → 발행!</div>"
    )

    img_idx = 0
    for i, post in enumerate(posts_data):
        color = cat_colors.get(post["category"], "#333")
        thumb_cid = "thumb_" + str(i)

        html += (
            "<div style='margin:0 0 32px;padding:24px;border:1px solid #eee;"
            "border-radius:16px;border-top:4px solid " + color + "'>"
            "<div style='margin-bottom:14px'>"
            "<span style='background:" + color + ";color:#fff;font-size:11px;"
            "padding:3px 10px;border-radius:20px;font-weight:700'>" + post["category"] + "</span>"
            "<span style='font-size:12px;color:#999;margin-left:8px'>" + str(i+1) + "번째 글</span></div>"
            "<h3 style='color:#222;margin:0 0 16px;font-size:17px'>" + post["title"] + "</h3>"
            "<div style='margin-bottom:16px;background:#f5f5f5;border-radius:8px;padding:12px'>"
            "<p style='font-size:12px;color:#f57c00;font-weight:700;margin:0 0 8px'>📸 썸네일</p>"
            "<img src='cid:" + thumb_cid + "' style='width:280px;border-radius:8px'></div>"
        )

        if post["images"]:
            html += (
                "<div style='margin-bottom:16px;background:#f0fff4;border-radius:8px;"
                "padding:12px;border:1px solid #c8e6c9'>"
                "<p style='font-size:12px;color:#388e3c;font-weight:700;margin:0 0 10px'>"
                "🖼 본문 이미지 " + str(len(post["images"])) + "장</p>"
                "<div style='display:flex;gap:8px;flex-wrap:wrap'>"
            )
            for j, img in enumerate(post["images"]):
                cid = "img_" + str(img_idx)
                html += (
                    "<div style='text-align:center'>"
                    "<img src='cid:" + cid + "' style='width:150px;border-radius:6px'>"
                    "<p style='font-size:10px;color:#999;margin:4px 0 0'>이미지" + str(j+1) + "</p></div>"
                )
                img_idx += 1
            html += "</div></div>"

        html += (
            "<div style='background:#f8f9ff;border-radius:8px;padding:16px;border:1px solid #e8eaf6'>"
            "<p style='font-size:12px;color:#5c6bc0;font-weight:700;margin:0 0 10px'>📝 본문</p>"
            "<pre style='white-space:pre-wrap;font-size:14px;color:#333;line-height:1.8;"
            "margin:0;font-family:sans-serif'>" + post["content"] + "</pre></div></div>"
        )

    html += "</body></html>"
    msg.attach(MIMEText(html, "html"))

    for i, post in enumerate(posts_data):
        att = MIMEImage(post["thumbnail_png"], _subtype="png")
        att.add_header("Content-ID", "<thumb_" + str(i) + ">")
        att.add_header("Content-Disposition", "attachment",
                       filename="썸네일_" + str(i+1) + "_" + post["category"] + ".png")
        msg.attach(att)

    total = 0
    for post in posts_data:
        for j, image in enumerate(post["images"]):
            att = MIMEImage(image["bytes"], _subtype="jpeg")
            att.add_header("Content-ID", "<img_" + str(total) + ">")
            att.add_header("Content-Disposition", "attachment",
                           filename="이미지_" + str(total+1) + ".jpg")
            msg.attach(att)
            total += 1

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, email_password)
        server.send_message(msg)
    print("이메일 전송 완료!")


count = int(os.environ.get("POST_COUNT", "2"))
date_str = datetime.date.today().strftime("%Y.%m.%d")
all_cats = list(CATEGORIES.keys())
selected = [all_cats[i % len(all_cats)] for i in range(count)]
posts_data = []

for i, category in enumerate(selected):
    persona = random.choice(PERSONAS)
    topic = random.choice(CATEGORIES[category])
    print("[" + str(i+1) + "/" + str(count) + "] " + category + " - " + topic)

    images = get_unsplash_images(topic, category, count=3)
    print("이미지 " + str(len(images)) + "장 준비")

    content = generate_post(category, topic, date_str, persona, len(images))

    title = topic
    for line in content.split("\n"):
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
            break

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
    if i < len(selected) - 1:
        time.sleep(3)

send_email(posts_data, date_str)
print("모든 작업 완료!")
