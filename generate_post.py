import anthropic
import datetime
import os
import random
import time
import urllib.request
import urllib.parse
import json

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")

topics = [
    "최신 AI 도구 활용법 완벽 가이드",
    "개발자 생산성을 높이는 VS Code 확장 프로그램 추천",
    "클라우드 서비스 AWS vs GCP vs Azure 비교",
    "사이버 보안 기초: 해킹으로부터 내 계정 지키는 법",
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
    "API란 무엇인가? 쉽게 설명하는 API 개념",
    "파이썬으로 업무 자동화하는 방법",
    "구글 애널리틱스로 블로그 트래픽 분석하기",
    "SEO 기초: 검색엔진 상위 노출 전략",
    "유튜브 알고리즘 완벽 분석",
    "재택근무 생산성을 높이는 툴 추천",
    "블록체인 기술 쉽게 이해하기",
    "메타버스란 무엇인가?",
    "스마트홈 구축하는 방법",
]

keyword_map = {
    "AI": "artificial intelligence technology",
    "VS Code": "coding programming computer",
    "클라우드": "cloud server technology",
    "보안": "cybersecurity technology",
    "ChatGPT": "artificial intelligence robot",
    "개발 도구": "developer tools laptop",
    "프로그래밍": "programming code laptop",
    "Mac": "apple macbook laptop",
    "Git": "programming code version",
    "노코드": "no code app development",
    "직업": "future work office",
    "SaaS": "software business technology",
    "웹 개발": "web development coding",
    "데이터": "data analysis chart",
    "스마트폰": "smartphone mobile technology",
    "리눅스": "linux terminal coding",
    "API": "api technology network",
    "파이썬": "python programming code",
    "애널리틱스": "analytics data dashboard",
    "SEO": "seo search engine marketing",
    "유튜브": "video content creator",
    "재택근무": "remote work home office",
    "블록체인": "blockchain cryptocurrency technology",
    "메타버스": "metaverse virtual reality",
    "스마트홈": "smart home iot technology",
}

def get_unsplash_image(topic):
    try:
        query = "technology computer"
        for key, val in keyword_map.items():
            if key in topic:
                query = val
                break
        encoded = urllib.parse.quote(query)
        url = f"https://api.unsplash.com/photos/random?query={encoded}&orientation=landscape&client_id={unsplash_key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())
            img_url = data["urls"]["regular"]
            photographer = data["user"]["name"]
            unsplash_link = data["links"]["html"]
            return img_url, photographer, unsplash_link
    except Exception as e:
        print(f"이미지 가져오기 실패: {e}")
        return None, None, None

count = int(os.environ.get("POST_COUNT", "1"))
os.makedirs("_posts", exist_ok=True)
used_topics = random.sample(topics, min(count, len(topics)))

for i, topic in enumerate(used_topics):
    date = datetime.date.today() - datetime.timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")

    img_url, photographer, unsplash_link = get_unsplash_image(topic)

    if img_url:
        image_md = f'\n![{topic}]({img_url})\n*사진: [{photographer}]({unsplash_link}) on Unsplash*\n'
    else:
        image_md = ""

    prompt = f"""다음 주제로 한국어 IT 블로그 글을 작성해줘: "{topic}"

아래 형식을 정확히 지켜서 작성해줘:

---
layout: post
title: "글 제목"
date: {date_str}
description: "한 줄 요약 (80자 이내)"
---

{image_md}

(본문 내용)

규칙:
- 본문은 최소 800자 이상
- 소제목(##)을 3개 이상 사용
- 독자에게 유용한 실용적인 내용
- 친근하고 읽기 쉬운 문체
- 맨 앞 --- 부터 시작해서 앞에 다른 텍스트 없이 바로 시작"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0].text
    slug = topic[:30].replace(" ", "-").replace("/", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    filename = f"_posts/{date_str}-{slug}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[{i+1}/{count}] 완료: {filename} (이미지: {'있음' if img_url else '없음'})")

    if i < len(used_topics) - 1:
        time.sleep(2)

print("모든 글 생성 완료!")import anthropic
import datetime
import os
import random
import time
import urllib.request
import urllib.parse
import json

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")

topics = [
    "최신 AI 도구 활용법 완벽 가이드",
    "개발자 생산성을 높이는 VS Code 확장 프로그램 추천",
    "클라우드 서비스 AWS vs GCP vs Azure 비교",
    "사이버 보안 기초: 해킹으로부터 내 계정 지키는 법",
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
    "API란 무엇인가? 쉽게 설명하는 API 개념",
    "파이썬으로 업무 자동화하는 방법",
    "구글 애널리틱스로 블로그 트래픽 분석하기",
    "SEO 기초: 검색엔진 상위 노출 전략",
    "유튜브 알고리즘 완벽 분석",
    "재택근무 생산성을 높이는 툴 추천",
    "블록체인 기술 쉽게 이해하기",
    "메타버스란 무엇인가?",
    "스마트홈 구축하는 방법",
]

# 주제에 맞는 영어 키워드 매핑
keyword_map = {
    "AI": "artificial intelligence technology",
    "VS Code": "coding programming computer",
    "클라우드": "cloud server technology",
    "보안": "cybersecurity technology",
    "ChatGPT": "artificial intelligence robot",
    "개발 도구": "developer tools laptop",
    "프로그래밍": "programming code laptop",
    "Mac": "apple macbook laptop",
    "Git": "programming code version",
    "노코드": "no code app development",
    "직업": "future work office",
    "SaaS": "software business technology",
    "웹 개발": "web development coding",
    "데이터": "data analysis chart",
    "스마트폰": "smartphone mobile technology",
    "리눅스": "linux terminal coding",
    "API": "api technology network",
    "파이썬": "python programming code",
    "애널리틱스": "analytics data dashboard",
    "SEO": "seo search engine marketing",
    "유튜브": "video content creator",
    "재택근무": "remote work home office",
    "블록체인": "blockchain cryptocurrency technology",
    "메타버스": "metaverse virtual reality",
    "스마트홈": "smart home iot technology",
}

def get_unsplash_image(topic):
    try:
        # 주제에 맞는 키워드 찾기
        query = "technology computer"
        for key, val in keyword_map.items():
            if key in topic:
                query = val
                break

        encoded = urllib.parse.quote(query)
        url = f"https://api.unsplash.com/photos/random?query={encoded}&orientation=landscape&client_id={unsplash_key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())
            img_url = data["urls"]["regular"]
            photographer = data["user"]["name"]
            unsplash_link = data["links"]["html"]
            return img_url, photographer, unsplash_link
    except Exception as e:
        print(f"이미지 가져오기 실패: {e}")
        return None, None, None

count = int(os.environ.get("POST_COUNT", "1"))
os.makedirs("_posts", exist_ok=True)
used_topics = random.sample(topics, min(count, len(topics)))

for i, topic in enumerate(used_topics):
    date = datetime.date.today() - datetime.timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")

    # 이미지 가져오기
    img_url, photographer, unsplash_link = get_unsplash_image(topic)

    # 이미지 마크다운 생성
    if img_url:
        image_md = f'\n![{topic}]({img_url})\n*사진: [{photographer}]({unsplash_link}) on Unsplash*\n'
    else:
        image_md = ""

    prompt = f"""다음 주제로 한국어 IT 블로그 글을 작성해줘: "{topic}"

아래 형식을 정확히 지켜서 작성해줘:

---
layout: post
title: "글 제목"
date: {date_str}
description: "한 줄 요약 (80자 이내)"
---

{image_md}

(본문 내용)

규칙:
- 본문은 최소 800자 이상
- 소제목(##)을 3개 이상 사용
- 독자에게 유용한 실용적인 내용
- 친근하고 읽기 쉬운 문체
- 맨 앞 --- 부터 시작해서 앞에 다른 텍스트 없이 바로 시작"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0].text
    slug = topic[:30].replace(" ", "-").replace("/", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    filename = f"_posts/{date_str}-{slug}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[{i+1}/{count}] 완료: {filename} (이미지: {'있음' if img_url else '없음'})")

    if i < len(used_topics) - 1:
        time.sleep(2)

print("모든 글 생성 완료!")import anthropic
import datetime
import os
import random

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

topics = [
    "최신 AI 도구 활용법 완벽 가이드",
    "개발자 생산성을 높이는 VS Code 확장 프로그램 추천",
    "클라우드 서비스 AWS vs GCP vs Azure 비교",
    "사이버 보안 기초: 해킹으로부터 내 계정 지키는 법",
    "ChatGPT 프롬프트 잘 쓰는 방법 10가지",
    "무료로 쓸 수 있는 최고의 개발 도구 모음",
    "2024년 주목해야 할 프로그래밍 언어 트렌드",
    "Mac 생산성을 2배 높이는 앱 추천",
    "Git 초보자를 위한 완벽 가이드",
    "노코드 툴로 앱 만드는 법",
    "AI가 바꾸는 직업의 미래",
    "스타트업이 사용하는 인기 SaaS 툴 모음",
    "웹 개발 입문자를 위한 로드맵",
    "데이터 분석 무료로 배우는 방법",
    "스마트폰 보안 설정 완벽 가이드",
]

topic = random.choice(topics)
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")

prompt = f"""다음 주제로 한국어 IT 블로그 글을 작성해줘: "{topic}"

아래 형식을 정확히 지켜서 작성해줘:

---
layout: post
title: "글 제목"
date: {date_str}
description: "한 줄 요약 (80자 이내)"
---

(본문 내용)

규칙:
- 본문은 최소 800자 이상
- 소제목(##)을 3개 이상 사용
- 독자에게 유용한 실용적인 내용
- 친근하고 읽기 쉬운 문체
- 맨 앞 --- 부터 시작해서 앞에 다른 텍스트 없이 바로 시작"""

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}],
)

content = message.content[0].text

slug = topic[:30].replace(" ", "-").replace("/", "-")
slug = "".join(c for c in slug if c.isalnum() or c == "-")
filename = f"_posts/{date_str}-{slug}.md"

os.makedirs("_posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"글 생성 완료: {filename}")
print(f"주제: {topic}")
