import anthropic
import datetime
import os
import random
import time
import urllib.request
import urllib.parse
import json
import glob

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")
youtube_key = os.environ.get("YOUTUBE_API_KEY")

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
    "애플 비전 프로 활용법",
    "챗GPT로 업무 자동화하는 방법",
    "유튜브 채널 성장 전략",
    "인스타그램 알고리즘 분석",
    "디지털 노마드 되는 방법",
    "온라인 부업으로 수익 만드는 법",
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
    "앱": "mobile app development",
    "해킹": "cybersecurity hacker",
    "유튜브": "youtube video content",
    "구글": "google technology",
    "애플": "apple technology",
}


def get_existing_topics():
    """이미 발행된 글 제목 수집 → 중복 방지"""
    existing = set()
    for filepath in glob.glob("_posts/*.md"):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("title:"):
                    title = line.replace("title:", "").strip().strip('"')
                    # 핵심 키워드만 추출 (5글자 이상 단어)
                    words = [w for w in title.split() if len(w) >= 5]
                    for word in words:
                        existing.add(word.lower())
    return existing


def is_duplicate(topic, existing_keywords):
    """주제가 기존 글과 중복인지 확인"""
    topic_words = [w for w in topic.split() if len(w) >= 5]
    for word in topic_words:
        if word.lower() in existing_keywords:
            return True
    return False


def get_youtube_trends():
    """YouTube IT 인기 영상 키워드 수집"""
    if not youtube_key:
        print("YouTube API 키 없음, 건너뜀")
        return []
    try:
        query = urllib.parse.quote("IT 기술 2025")
        url = ("https://www.googleapis.com/youtube/v3/search"
               "?part=snippet&q=" + query +
               "&type=video&order=viewCount&regionCode=KR"
               "&relevanceLanguage=ko&maxResults=20"
               "&key=" + youtube_key)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())

        topics = []
        for item in data.get("items", []):
            title = item["snippet"]["title"]
            # 너무 짧거나 광고성 제목 제외
            if len(title) > 10 and "광고" not in title and "협찬" not in title:
                topics.append(title[:40] + " 완벽 정리")

        print("YouTube 트렌드 수집: " + str(len(topics)) + "개")
        return topics
    except Exception as e:
        print("YouTube 수집 실패: " + str(e))
        return []


def get_google_trends():
    """Google Trends 한국 IT 트렌드 수집"""
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
            if title and "Google" not in title and len(title) > 2:
                titles.append(title)
            start = e + 1

        it_keywords = ["AI", "GPT", "앱", "구글", "애플", "삼성", "메타",
                      "스마트", "IT", "테크", "소프트웨어", "게임", "클라우드",
                      "챗봇", "로봇", "드론", "반도체", "스타트업", "유튜브"]

        it_trends = []
        for title in titles:
            for kw in it_keywords:
                if kw.lower() in title.lower():
                    it_trends.append(title + " 트렌드 분석")
                    break

        print("Google 트렌드 수집: " + str(len(it_trends)) + "개")
        return it_trends
    except Exception as e:
        print("Google 트렌드 수집 실패: " + str(e))
        return []


def get_unsplash_image(topic):
    try:
        query = "technology computer"
        for key, val in keyword_map.items():
            if key in topic:
                query = val
                break
        encoded = urllib.parse.quote(query)
        url = ("https://api.unsplash.com/photos/random?query=" + encoded +
               "&orientation=landscape&client_id=" + unsplash_key)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())
            return data["urls"]["regular"], data["user"]["name"], data["links"]["html"]
    except Exception as e:
        print("이미지 가져오기 실패: " + str(e))
        return None, None, None


# 기존 글 키워드 수집
existing_keywords = get_existing_topics()
print("기존 글 키워드: " + str(len(existing_keywords)) + "개 로드")

# 트렌드 수집 (YouTube + Google Trends + 기본)
youtube_topics = get_youtube_trends()
google_topics = get_google_trends()
all_topics = youtube_topics + google_topics + fallback_topics
all_topics = list(dict.fromkeys(all_topics))  # 중복 제거

# 중복 제거된 토픽만 선택
unique_topics = [t for t in all_topics if not is_duplicate(t, existing_keywords)]
print("사용 가능한 토픽: " + str(len(unique_topics)) + "개 (중복 제거 후)")

if not unique_topics:
    print("모든 토픽이 중복됨, 기본 토픽에서 랜덤 선택")
    unique_topics = fallback_topics

count = int(os.environ.get("POST_COUNT", "1"))
os.makedirs("_posts", exist_ok=True)
selected = random.sample(unique_topics, min(count, len(unique_topics)))

for i, topic in enumerate(selected):
    date = datetime.date.today() - datetime.timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")

    img_url, photographer, unsplash_link = get_unsplash_image(topic)

    if img_url:
        image_md = "\n![" + topic + "](" + img_url + ")\n*사진: [" + photographer + "](" + unsplash_link + ") on Unsplash*\n"
    else:
        image_md = ""

    prompt = "다음 주제로 한국어 IT 블로그 글을 작성해줘: \"" + topic + "\"\n\n"
    prompt += "아래 형식을 정확히 지켜서 작성해줘:\n\n"
    prompt += "---\n"
    prompt += "layout: post\n"
    prompt += "title: \"글 제목\"\n"
    prompt += "date: " + date_str + "\n"
    prompt += "description: \"한 줄 요약 (80자 이내)\"\n"
    prompt += "---\n"
    prompt += image_md + "\n"
    prompt += "본문 내용을 여기에 작성\n\n"
    prompt += "규칙:\n"
    prompt += "- 본문은 최소 800자 이상\n"
    prompt += "- 소제목(##)을 3개 이상 사용\n"
    prompt += "- 트렌드 키워드 자연스럽게 포함\n"
    prompt += "- 독자에게 유용한 실용적인 내용\n"
    prompt += "- 친근하고 읽기 쉬운 문체\n"
    prompt += "- 맨 앞 --- 부터 시작해서 앞에 다른 텍스트 없이 바로 시작"

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0].text
    slug = topic[:30].replace(" ", "-").replace("/", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    filename = "_posts/" + date_str + "-" + slug + ".md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print("[" + str(i+1) + "/" + str(count) + "] 완료: " + filename)

    if i < len(selected) - 1:
        time.sleep(2)

print("모든 글 생성 완료!")
