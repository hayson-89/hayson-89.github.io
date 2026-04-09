import os
import time
import urllib.request
import urllib.parse
import json
from playwright.sync_api import sync_playwright
from sports_config import TOPIC_KEYWORDS, DEFAULT_KEYWORDS, THUMBNAIL_STYLES, CATEGORY_ICONS

unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")


def get_topic_keywords(topic, category):
    for key, keywords in TOPIC_KEYWORDS.items():
        if key in topic:
            return keywords
    return DEFAULT_KEYWORDS.get(category, ["sports athlete"])


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
            url = ("https://api.unsplash.com/photos/random?query=" + encoded
                   + "&orientation=landscape&client_id=" + unsplash_key)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode())
            img_url = data["urls"]["regular"]
            img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=20) as img_res:
                img_bytes = img_res.read()
            print("이미지" + str(i + 1) + " 완료 (" + str(len(img_bytes)) + " bytes)")
            images.append({
                "bytes": img_bytes,
                "photographer": data["user"]["name"],
                "link": data["links"]["html"],
                "query": query,
            })
            time.sleep(1)
        except Exception as e:
            print("이미지" + str(i + 1) + " 실패: " + str(e))

    return images


def make_thumbnail_html(category, title, date_str):
    style = THUMBNAIL_STYLES.get(category, THUMBNAIL_STYLES["스포츠뉴스"])
    icon = CATEGORY_ICONS.get(category, "🏃")
    short_title = title[:28] + "..." if len(title) > 28 else title

    return (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
        "<style>"
        "@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=swap');"
        "*{margin:0;padding:0;box-sizing:border-box}"
        "body{width:600px;height:400px;overflow:hidden}"
        ".t{width:600px;height:400px;background:" + style["bg"] + ";position:relative;"
        "display:flex;align-items:flex-end;font-family:'Noto Sans KR',sans-serif}"
        ".o{position:absolute;inset:0;background:rgba(0,0,0,0.35)}"
        ".d1{position:absolute;top:-40px;right:-40px;width:200px;height:200px;"
        "border-radius:50%;background:rgba(255,255,255,0.06)}"
        ".d2{position:absolute;bottom:-30px;left:-30px;width:140px;height:140px;"
        "border-radius:50%;background:rgba(255,255,255,0.04)}"
        ".ic{position:absolute;top:20px;right:20px;z-index:2;width:50px;height:50px;"
        "border-radius:50%;background:rgba(255,255,255,0.15);"
        "display:flex;align-items:center;justify-content:center;font-size:26px}"
        ".c{position:relative;z-index:2;padding:24px;width:100%}"
        ".ct{display:inline-block;font-size:12px;font-weight:700;padding:5px 12px;"
        "border-radius:20px;margin-bottom:12px;background:" + style["cat_bg"] + ";"
        "color:" + style["cat_color"] + ";letter-spacing:1px}"
        ".tt{font-size:26px;font-weight:700;color:#fff;line-height:1.4;margin:0 0 12px;"
        "text-shadow:0 2px 4px rgba(0,0,0,0.5)}"
        ".m{display:flex;align-items:center;gap:8px}"
        ".dt{font-size:12px;color:rgba(255,255,255,0.7)}"
        ".dv{width:1px;height:10px;background:rgba(255,255,255,0.4)}"
        ".bl{font-size:12px;color:rgba(255,255,255,0.7)}"
        "</style></head><body>"
        "<div class='t'>"
        "<div class='o'></div><div class='d1'></div><div class='d2'></div>"
        "<div class='ic'>" + icon + "</div>"
        "<div class='c'>"
        "<span class='ct'>" + category + "</span>"
        "<p class='tt'>" + short_title + "</p>"
        "<div class='m'>"
        "<span class='dt'>" + date_str + "</span>"
        "<span class='dv'></span>"
        "<span class='bl'>생활스포츠 블로그</span>"
        "</div></div></div>"
        "</body></html>"
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
