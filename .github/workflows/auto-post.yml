import anthropic
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
