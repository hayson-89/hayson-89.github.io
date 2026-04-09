CATEGORIES = {
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

TOPIC_KEYWORDS = {
    "손흥민": ["son heungmin football", "tottenham soccer", "korean soccer player"],
    "KBO": ["baseball korea", "baseball stadium", "baseball game"],
    "NBA": ["basketball nba", "basketball game", "basketball player dunking"],
    "K리그": ["korean football league", "soccer match korea", "football stadium"],
    "EPL": ["premier league football", "english soccer", "football match stadium"],
    "야구 국가대표": ["korea baseball team", "baseball pitcher", "baseball national team"],
    "배구": ["volleyball game", "volleyball player", "volleyball match"],
    "UFC": ["mma fighting", "ufc fighter", "martial arts combat"],
    "축구 포지션": ["soccer tactics", "football formation", "soccer player position"],
    "헬스": ["gym workout", "fitness training", "weight lifting gym"],
    "수영": ["swimming pool", "freestyle swimming", "swimmer underwater"],
    "골프": ["golf swing", "golf course", "golfer playing"],
    "달리기": ["running marathon", "runner road", "jogging outdoor"],
    "배드민턴": ["badminton court", "badminton player", "badminton smash"],
    "등산": ["hiking mountain", "mountain trail", "hiker trekking"],
    "자전거": ["cycling road", "bicycle rider", "mountain biking"],
    "생활체육대회": ["sports community event", "amateur sports competition", "sports festival"],
    "전국체육대회": ["national sports games", "athletics competition", "sports tournament"],
    "스포츠 센터": ["sports center indoor", "fitness center", "sports facility"],
    "마라톤 대회": ["marathon race", "marathon runners road", "running competition"],
    "동호회": ["sports club team", "amateur sports team", "community sports"],
    "스포츠 용품": ["sports equipment store", "athletic gear", "sports shoes"],
    "축구를 시작": ["kids playing soccer", "youth football", "soccer beginners"],
    "야구팀": ["baseball team", "baseball players dugout", "amateur baseball"],
    "마라톤 완주": ["marathon finish line", "runner crossing finish", "marathon achievement"],
    "슬럼프": ["athlete determination", "sports comeback", "perseverance sports"],
    "정신 건강": ["meditation sports", "wellness exercise", "mental health fitness"],
}

DEFAULT_KEYWORDS = {
    "스포츠뉴스": ["sports news", "athlete competition", "sports stadium"],
    "스포츠정보": ["sports training", "fitness workout", "athlete exercise"],
    "스포츠소식": ["sports event", "sports community", "athletic competition"],
    "스포츠이야기": ["sports lifestyle", "team sports", "outdoor sports"],
}

THUMBNAIL_STYLES = {
    "스포츠뉴스": {"bg": "linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)", "cat_bg": "#e63946", "cat_color": "#fff"},
    "스포츠정보": {"bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)", "cat_bg": "#f4a261", "cat_color": "#1a1a1a"},
    "스포츠소식": {"bg": "linear-gradient(135deg,#2d1b00 0%,#8b4513 50%,#d2691e 100%)", "cat_bg": "#f4a261", "cat_color": "#1a1a1a"},
    "스포츠이야기": {"bg": "linear-gradient(135deg,#0d2137 0%,#1a4a6e 50%,#0077b6 100%)", "cat_bg": "#00b4d8", "cat_color": "#fff"},
}

CATEGORY_ICONS = {
    "스포츠뉴스": "⚡",
    "스포츠정보": "📋",
    "스포츠소식": "📢",
    "스포츠이야기": "💬",
}

PERSONAS = [
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
