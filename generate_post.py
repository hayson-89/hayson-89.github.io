import datetime,os,random,time,glob,urllib.request,urllib.parse,json,requests

gemini_key=os.environ.get("GEMINI_API_KEY")
unsplash_key=os.environ.get("UNSPLASH_ACCESS_KEY")

topics=["최신 AI 도구 활용법 완벽 가이드","개발자 생산성을 높이는 VS Code 확장 프로그램 추천","클라우드 서비스 AWS vs GCP vs Azure 비교","사이버 보안 기초 해킹으로부터 내 계정 지키는 법","ChatGPT 프롬프트 잘 쓰는 방법 10가지","무료로 쓸 수 있는 최고의 개발 도구 모음","2025년 주목해야 할 프로그래밍 언어 트렌드","Mac 생산성을 2배 높이는 앱 추천","Git 초보자를 위한 완벽 가이드","노코드 툴로 앱 만드는 법","AI가 바꾸는 직업의 미래","스타트업이 사용하는 인기 SaaS 툴 모음","웹 개발 입문자를 위한 로드맵","데이터 분석 무료로 배우는 방법","스마트폰 보안 설정 완벽 가이드","리눅스 명령어 초보자 가이드","파이썬으로 업무 자동화하는 방법","구글 애널리틱스로 블로그 트래픽 분석하기","SEO 기초 검색엔진 상위 노출 전략","재택근무 생산성을 높이는 툴 추천","블록체인 기술 쉽게 이해하기","메타버스란 무엇인가","스마트홈 구축하는 방법","구글 Gemini AI 완벽 가이드","챗GPT로 업무 자동화하는 방법","디지털 노마드 되는 방법","온라인 부업으로 수익 만드는 법","유튜브 채널 성장 전략","구글 검색 잘하는 방법","윈도우 단축키 완벽 정리"]

kwmap={"AI":"artificial intelligence technology","VS Code":"coding programming computer","클라우드":"cloud server technology","보안":"cybersecurity technology","ChatGPT":"artificial intelligence robot","개발":"developer tools laptop","프로그래밍":"programming code laptop","Mac":"apple macbook laptop","Git":"programming code version","노코드":"no code app development","직업":"future work office","SaaS":"software business technology","웹":"web development coding","데이터":"data analysis chart","스마트폰":"smartphone mobile technology","리눅스":"linux terminal coding","파이썬":"python programming code","SEO":"seo search engine marketing","재택":"remote work home office","블록체인":"blockchain cryptocurrency technology","메타버스":"metaverse virtual reality","스마트홈":"smart home iot technology","GPT":"artificial intelligence chatbot","Gemini":"google ai technology","유튜브":"youtube video content","디지털":"digital nomad laptop","부업":"online business laptop"}

def call_gemini(prompt):
    for model in ["gemini-2.0-flash","gemini-1.5-flash","gemini-1.5-flash-8b"]:
        try:
            url="https://generativelanguage.googleapis.com/v1beta/models/"+model+":generateContent?key="+gemini_key
            r=requests.post(url,json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.7,"maxOutputTokens":2048}},timeout=30)
            d=r.json()
            if "candidates" in d:
                print("모델:"+model)
                return d["candidates"][0]["content"]["parts"][0]["text"]
            print(model+" 실패:"+str(d.get("error",{}).get("message",""))[:80])
            time.sleep(3)
        except Exception as e:
            print("오류:"+str(e))
            time.sleep(3)
    return None

def get_image(topic):
    if not unsplash_key:
        return None,None,None
    try:
        q="technology computer"
        for k,v in kwmap.items():
            if k in topic:
                q=v;break
        url="https://api.unsplash.com/photos/random?query="+urllib.parse.quote(q)+"&orientation=landscape&client_id="+unsplash_key
        with urllib.request.urlopen(urllib.request.Request(url),timeout=10) as r:
            d=json.loads(r.read().decode())
        return d["urls"]["regular"],d["urls"]["small"],d["user"]["name"]
    except:
        return None,None,None

def get_trends():
    try:
        url="https://trends.google.com/trending/rss?geo=KR"
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=10) as r:
            c=r.read().decode("utf-8")
        kws=["AI","GPT","앱","구글","애플","삼성","스마트","IT","테크","클라우드","반도체"]
        result=[]
        s=0
        while True:
            i=c.find("<title>",s)
            if i==-1:break
            e=c.find("</title>",i)
            t=c[i+7:e].replace("<![CDATA[","").replace("]]>","").strip()
            if t and "Google" not in t and len(t)>2:
                for k in kws:
                    if k in t:result.append(t+" 완벽 분석");break
            s=e+1
        print("트렌드:"+str(len(result))+"개")
        return result
    except:
        return []

def existing_titles():
    s=set()
    for f in glob.glob("_posts/*.md"):
        with open(f,"r",encoding="utf-8") as fp:
            for line in fp:
                if line.startswith("title:"):
                    for w in line.replace("title:","").strip().strip('"').split():
                        if len(w)>=5:s.add(w.lower())
    return s

count=int(os.environ.get("POST_COUNT","1"))
date_str=datetime.date.today().strftime("%Y-%m-%d")
os.makedirs("_posts",exist_ok=True)
existing=existing_titles()
pool=[t for t in list(dict.fromkeys(get_trends()+topics)) if not any(len(w)>=5 and w.lower() in existing for w in t.split())]
if not pool:pool=topics
selected=random.sample(pool,min(count,len(pool)))

for i,topic in enumerate(selected):
    print("["+str(i+1)+"/"+str(count)+"] "+topic[:40])
    lg,sm,ph=get_image(topic)
    tl=('thumbnail: "'+sm+'"\n') if sm else ""
    ib=("\n\n!["+topic+"]("+lg+")\n*© "+ph+" / Unsplash*\n\n") if lg else ""
    prompt=("다음 주제로 한국어 IT 블로그 글을 작성해줘: \""+topic+"\"\n\n반드시 아래 형식 그대로 출력해. 앞에 다른 텍스트 절대 없이:\n\n---\nlayout: post\ntitle: \"글 제목\"\ndate: "+date_str+"\ndescription: \"한 줄 요약 (80자 이내)\"\n"+tl+"---\n"+ib+"\n본문 내용\n\n규칙:\n- 본문 800자 이상\n- 소제목(##) 3개 이상\n- 실용적이고 유익한 내용\n- 친근한 문체\n- 이모지 금지")
    content=call_gemini(prompt)
    if not content:print("생성 실패");continue
    if "---" in content:content=content[content.find("---"):]
    content=content.replace("```yaml","").replace("```markdown","").replace("```","")
    slug="".join(c for c in topic[:30].replace(" ","-") if c.isalnum() or c=="-")
    fn="_posts/"+date_str+("" if i==0 else "-"+str(i+1))+"-"+slug+".md"
    with open(fn,"w",encoding="utf-8") as f:f.write(content)
    print("완료:"+fn)
    if i<len(selected)-1:time.sleep(2)

print("모든 글 생성 완료!")
