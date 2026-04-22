import datetime
import os
import random
import time
import glob
import urllib.request
import urllib.parse
import json
import requests

gemini_key = os.environ.get("GEMINI_API_KEY")
unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")

fallback_topics = [
    "최신 AI 도구 활용법 완벽 가이드",
    "개발자 생산성을 높이는 VS Code 확장 프로그램 추천",
    "클라우드 서비스 AWS vs GCP vs Azure 비교",
    "사이버 보안 기초 해킹으로부터 내 계정 지키는 법",
    "ChatGPT 프롬프트 잘 쓰는 방법 10가지",
    "무료로 쓸 수 있는 최고의 개발 도구 모음",
    "2025년 주목해야 할 프로그래밍 언어 트렌드",
    "Mac 생산성을 2배 높이는 앱 추천",
    "Git 초보자를 위한 완벽 가이드",
    "노코드 툴로 앱 만드는 법",
    "AI가 바꾸는 직업의 미래",
    "스타트업이 사용하는 인기 SaaS 툴 모음",
    "웹 개발 입문자를 위한 로드맵",
    "데이터 분석 무료로 배우는 방법",
    "스마트폰 보안 설정 완벽 가이드",
    "리눅스 명령어 초보자 가이드",
    "파이썬으로 업무 자동화하는 방법",
    "구글 애널리틱스로 블로그 트래픽 분석하기",
    "SEO 기초 검색엔진 상위 노출 전략",
    "재택근무 생산성을 높이는 툴 추천",
    "블록체인 기술 쉽게 이해하기",
    "메타버스란 무엇인가",
    "스마트홈 구축하는 방법",
    "구글 Gemini AI 완벽 가이드",
    "챗GPT로 업무 자동화하는 방법",
    "디지털 노마드 되는 방법",
    "온라인 부업으로 수익 만드는 법",
    "유튜브 채널 성장 전략",
    "구글 검색 잘하는 방법",
    "윈도우 단축키 완벽 정리",
]

keyword_map = {
    "AI": "artificial intelligence technology",
    "VS Code": "coding programming computer",
    "클라우드": "cloud server technology",
    "보안": "cybersecurity technology",
    "ChatGPT": "artificial intelligence robot",
    "개발": "developer tools laptop",
    "프로그래밍": "programming code laptop",
    "Mac": "apple macbook laptop",
    "Git": "programming code version",
    "노코드": "no code app development",
    "직업": "future work office",
    "SaaS": "software business technology",
    "웹": "web development coding",
    "데이터": "data analysis chart",
    "스마트폰": "smartphone mobile technology",
    "리눅스": "linux terminal coding",
    "파이썬": "python programming code",
    "SEO": "seo search engine marketing",
    "재택": "remote work home office",
    "블록체인": "blockchain cryptocurrency technology",
    "메타버스": "metaverse virtual reality",
    "스마트홈": "smart home iot technology",
    "GPT": "artificial intelligence chatbot",
    "Gemini": "google ai technology",
    "유튜브": "youtube video content",
    "디지털": "digital nomad laptop",
    "부업": "online business laptop",
}


def call_gemini(prompt):
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-1.5-flash:generateContent?key=" + gemini_key)
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    res = requests.post(url, json=body, timeout=30)
    data = res.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Gemini 오류: " + str(e))
        return None


def get_trending_topics():
    try:
        url = "https://trends.google.com/trending/rss?geo=KR"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            content = res.read().decode("utf-8")
        titles = []
        start = 0
        while True:
            s = content.find("<title>", start)
            if s == -1:
                break
            e = content.find("</title>", s)
            title = content[s+7:e].strip()
            title = title.replace("<![CDATA[", "").replace("]]>", "").strip()
            if title and "Google" not in title and len(title) > 2:
                titles.append(title)
            start = e + 1
        it_keywords = ["AI", "GPT", "앱", "구글", "애플", "삼성", "메타",
                       "스마트", "IT", "테크", "소프트웨어", "게임", "클라우드",
                       "챗봇", "로봇", "반도체", "스타트업"]
        it_trends = []
        for title in titles:
            for kw in it_keywords:
                if kw.lower() in title.lower():
                    it_trends.append(title + " 완벽 분석")
                    break
        print("트렌드 수집: " + str(len(it_trends)) + "개")
        return it_trends
    except Exception as e:
        print("트렌드 수집 실패: " + str(e))
        return []


def get_unsplash_image(topic):
    if not unsplash_key:
        return None, None, None
    try:
        query = "technology computer"
        for key, val in keyword_map.items():
            if key in topic:
                query = val
                break
        encoded = urllib.parse.quote(query)
        url = ("https://api.unsplash.com/photos/random?query=" + encoded
               + "&orientation=landscape&client_id=" + unsplash_key)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())
        return data["urls"]["regular"], data["urls"]["small"], data["user"]["name"]
    except Exception as e:
        print("이미지 실패: " + str(e))
        return None, None, None


def get_existing_titles():
    titles = set()
    for filepath in glob.glob("_posts/*.md"):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("title:"):
                    title = line.replace("title:", "").strip().strip('"')
                    for w in title.split():
                        if len(w) >= 5:
                            titles.add(w.lower())
    return titles


def is_duplicate(topic, existing):
    for w in topic.split():
        if len(w) >= 5 and w.lower() in existing:
            return True
    return False


count = int(os.environ.get("POST_COUNT", "1"))
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")
os.makedirs("_posts", exist_ok=True)

existing = get_existing_titles()
trending = get_trending_topics()
all_topics = list(dict.fromkeys(trending + fallback_topics))
unique = [t for t in all_topics if not is_duplicate(t, existing)]
pool = unique if unique else fallback_topics
selected = random.sample(pool, min(count, len(pool)))

for i, topic in enumerate(selected):
    print("[" + str(i+1) + "/" + str(count) + "] " + topic[:40])

    img_large, img_small, photographer = get_unsplash_image(topic)

    # thumbnail front matter
    thumbnail_line = ('thumbnail: "' + img_small + '"\n') if img_small else ""

    # 본문 이미지 블록
    img_block = ""
    if img_large:
        img_block = "\n\n![" + topic + "](" + img_large + ")\n*© " + photographer + " / Unsplash*\n\n"

    prompt = ("다음 주제로 한국어 IT 블로그 글을 작성해줘: \"" + topic + "\"\n\n"
              "반드시 아래 형식 그대로 출력해. 앞에 다른 텍스트 절대 없이:\n\n"
              "---\n"
              "layout: post\n"
              "title: \"글 제목\"\n"
              "date: " + date_str + "\n"
              "description: \"한 줄 요약 (80자 이내)\"\n"
              + thumbnail_line +
              "---\n"
              + img_block +
              "\n본문 내용\n\n"
              "규칙:\n"
              "- 본문 800자 이상\n"
              "- 소제목(##) 3개 이상\n"
              "- 실용적이고 유익한 내용\n"
              "- 친근한 문체\n"
              "- 이모지 금지")

    content = call_gemini(prompt)
    if not content:
        print("생성 실패, 건너뜀")
        continue

    if "---" in content:
        content = content[content.find("---"):]

    # 코드블록 제거 (```yaml 등)
    content = content.replace("```yaml", "").replace("```markdown", "").replace("```", "")

    slug = topic[:30].replace(" ", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    suffix = "" if i == 0 else "-" + str(i+1)
    filename = "_posts/" + date_str + suffix + "-" + slug + ".md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print("완료: " + filename)
    if i < len(selected) - 1:
        time.sleep(1)

print("모든 글 생성 완료!")
