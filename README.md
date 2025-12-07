# 🤖 AI 탭 정리 에이전트 (Chrome Extension)

컨텍스트 인식 AI 에이전트가 현재 작업 중인 탭을 파악하고, 관련 없는 오래된 탭을 자동으로 정리해주는 Chrome 확장 프로그램

## ✨ 주요 기능

- 🧠 **AI 컨텍스트 인식**: 현재 활성 탭을 분석하여 작업 맥락 파악
- 🎯 **스마트 정리**: 관련 없는 카테고리의 오래된 탭 자동 선별
- ⏰ **사용자 지정 시간**: 기준 시간을 직접 설정 가능 (기본 60분)
- 💾 **백업 저장**: 닫은 탭 정보를 자동으로 파일로 백업
- 🔧 **Pydantic AI Agent**: 도구 기반 에이전트 아키텍처

## 🏗️ 기술 스택

### Backend
- **FastAPI**: 비동기 웹 서버
- **Pydantic AI**: AI 에이전트 프레임워크
- **Google Gemini 2.0**: LLM 모델
- **Python 3.11+**

### Frontend
- **Chrome Extension API**: Manifest V3
- **Vanilla JavaScript**: 가벼운 UI

### Architecture
- **DTO/Entity 패턴**: 계층 분리
- **Agent with Tools**: find_old_tabs 도구 활용
- **CORS 지원**: Extension ↔ Server 통신

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/tab-organizer.git
cd tab-organizer
```

### 2. Python 환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
# .env 파일 생성
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. 서버 실행
```bash
python server.py
```

### 5. Chrome 확장 프로그램 로드
1. Chrome 주소창에 `chrome://extensions/` 입력
2. 우측 상단 "개발자 모드" 활성화
3. "압축해제된 확장 프로그램을 로드합니다" 클릭
4. `chrome-extension` 폴더 선택

## 🚀 사용 방법

1. **서버 실행**: `python server.py`
2. **확장 프로그램 클릭**: Chrome 툴바의 확장 아이콘
3. **시간 설정**: 기준 시간 입력 (분 단위)
4. **스마트 정리 클릭**: AI가 자동으로 분석 및 정리

## 🧠 AI Agent 구조
```
Extension (popup.js)
  ↓ {focused_tabs, all_tabs, time_threshold}
FastAPI Server
  ↓ TabContext 생성 (DTO → Entity)
Pydantic AI Agent
  ↓ find_old_tabs(minutes) 도구 호출
  ↓ 카테고리 분석 + 관련성 판단
  ↓ [닫을 탭 ID 리스트] 반환
Server
  ↓ 백업 파일 저장
  ↓ {tab_ids} 반환
Extension
  ↓ 사용자 확인
  ↓ chrome.tabs.remove(tab_ids)
```

## 📂 프로젝트 구조
```
tab-organizer/
├── agent.py              # AI 에이전트 정의
├── models.py             # Pydantic 모델 (DTO, Entity)
├── server.py             # FastAPI 서버
├── file_handler.py       # 백업 파일 저장
├── chrome-extension/
│   ├── manifest.json     # 확장 프로그램 설정
│   ├── popup.html        # UI
│   └── popup.js          # 로직
├── requirements.txt
├── .env
└── README.md
```

## 🎯 카테고리 기준

- 💼 **work**: 업무, 개발 도구, 문서 편집
- 📚 **study**: 학습, 튜토리얼, 강의
- 🎬 **entertainment**: YouTube, Netflix, 게임
- 💬 **social**: SNS, 메신저, 커뮤니티
- 🛒 **shopping**: 쇼핑몰, 가격 비교
- 📌 **etc**: 기타

## 🔧 트러블슈팅

### 1. "정리할 탭이 없습니다"
- 모든 탭이 최근에 접근된 경우
- 기준 시간을 줄여보세요 (예: 30분)

### 2. "서버 오류: 500"
- `.env` 파일에 `GOOGLE_API_KEY` 확인
- 서버가 실행 중인지 확인 (`http://localhost:8000`)

### 3. CORS 오류
- 서버의 CORS 설정 확인
- `allow_origins=["*"]`

## 📝 개발 과정

- DTO/Entity 패턴 적용으로 계층 분리
- `**dict` 언패킹으로 Pydantic 모델 변환
- Agent Instructions 최적화
- 상수 추출로 유지보수성 향상

## 🤝 기여

Issues와 Pull Requests는 언제나 환영입니다!

## 📄 라이선스

MIT License

