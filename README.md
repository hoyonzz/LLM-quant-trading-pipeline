# 📈 LLM-Quant Strategy Pipeline (LQSP)

> **"지능형 에이전트 기반의 데이터 통합 및 투자 전략 수립 자동화 파이프라인"**

본 프로젝트는 금융 시장의 감정적 편향을 제거하기 위해 **LLM(Gemini 1.5 Pro)**의 전략적 사고와 **증권사/AI API의 정밀 데이터**를 결합한 **Semi-Auto Trading 인프라**입니다.

---

## 🏗 1. System Architecture

본 시스템은 'AI Captain' 페르소나를 중심으로 Macro(정성)와 Micro(정량) 데이터를 통합 분석합니다.

### **[Data Flow]**
1.  **Macro Analysis (Qualitative)**: **Perplexity API (Sonar Large Online)** → Python Backend → **Google Sheets** (Logging).
2.  **Micro Analysis (Quantitative)**: **KIS REST API** (실시간 시세, 수급, 기술적 지표) → Python Backend.
3.  **Strategy Engine (AI Captain)**:
    *   **Gemini 2.0 Flash**: 이종 데이터 전처리 및 데이터 무결성 검증.
    *   **Gemini 1.5 Pro**: 'AI Captain' 페르소나를 기반으로 최종 투자 전략(Signal, Action Plan) 수립.
4.  **Delivery**: **Discord Webhook**을 통한 구조화된 **Embed** 메시지 전송.

---

## 🛠 2. Tech Stack & Tools

### **Backend & APIs**
- **Language**: Python 3.10+
- **Finance API**: 한국투자증권 KIS Developers (REST API, WebSocket)
- **AI Models**: Gemini 1.5 Pro / 2.0 Flash, **Perplexity API (Sonar Large)**
- **Database**: Google Sheets (Lightweight Data Lake)

### **Infrastructure & DevOps**
- **Automation**: **GitHub Actions** (Scheduled Task Runner)
- **Communication**: Discord API (Notification & Interactive Bot)
- **Secret Management**: Python-dotenv (.env)

---

## 📌 3. Project Roadmap & Milestones

### ✅ v0.1.0: Foundation (Completed)
- [x] 프로젝트 인프라 및 가상환경(venv) 구축.
- [x] KIS OAuth 2.0 인증 모듈 (`auth.py`) 개발 (Token Caching 포함).
- [x] Discord 알림 엔진 (`discord_bot.py`) 및 Embed 레이아웃 구현.

### 🟡 v0.2.0: Advanced Data Pipeline (Current)
- [ ] **Perplexity API 연동**: 실시간 매크로 리서치 자동화 (`researcher.py`).
- [ ] **Google Sheets API 연동**: 리서치 데이터 로깅 및 파이썬 연동 (`gsheet_manager.py`).
- [ ] 데이터 정규화(Data Normalization) 프로세스 구축.

### 🟠 v0.3.0: Intelligence Strategy Engine
- [ ] 'AI Captain' 페르소나 최적화 및 전략 수립 프롬프트 통합.
- [ ] KIS API 기반 기술적 지표(이평선, RSI 등) 추출 모듈 완성.

### 🔴 v0.4.0: Tactical Real-time Mode
- [ ] **Async/WebSocket** 기반 실시간 호가 스트리밍.
- [ ] **Interactive Discord Bot**: AI Captain과의 실시간 전략 대화 기능.

---

## 🔥 4. Engineering Challenges & Solutions

### ✅ **[Issue #1] 데이터 수집 아키텍처 최적화 (v0.2.0)**
*   **Problem**: 초기 기획(Email-GAS 방식) 시 퍼플렉시티 이메일 요약본의 정보 밀도가 낮아 AI Captain의 판단 근거가 부족해지는 현상 발생.
*   **Solution**: **Perplexity API**를 직접 호출하는 방식으로 아키텍처 변경. 이를 통해 Full-text 리서치 데이터를 확보하고 파이프라인 단계를 단축하여 시스템 복잡도 해결.

### ✅ **[Issue #2] 토큰 매니징 및 API 최적화 (v0.1.0)**
*   **Problem**: 24시간 만료 토큰 관리 및 빈번한 API 호출로 인한 서버 부하 위험.
*   **Solution**: 로컬 캐싱 전략을 도입하여 유효성 검증 후 필요 시에만 토큰을 재발급하는 로직 구현.

---

## 📂 5. Directory Structure
```text
.
├── src/
│   ├── auth.py          # KIS API 인증 및 토큰 관리
│   ├── discord_bot.py   # 디스코드 알림 및 Embed 포맷팅
│   ├── gsheet_manager.py # 구글 시트 읽기/쓰기 모듈 (v0.2.0)
│   └── researcher.py     # Perplexity API 리서치 모듈 (v0.2.0)
├── data/                # 토큰 및 로컬 캐시 (Git 제외)
├── google_key.json      # Google Service Account Key (Git 제외)
├── .env                 # API 키 관리
└── .gitignore           # 보안 설정
