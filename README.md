# 📈 LLM-Quant Strategy Pipeline (LQSP)

> **"지능형 에이전트 기반의 데이터 통합 및 투자 전략 수립 자동화 파이프라인"**

본 프로젝트는 불확실성이 높은 금융 시장에서 개인 투자자의 감정적 편향을 배제하고, **LLM(Gemini 1.5 Pro)의 전략적 추론**과 **증권사 REST API의 정량 데이터**를 결합하여 수익을 창출하는 **Semi-Auto Trading 인프라**를 구축합니다.

---

## 🏛 1. System Architecture

본 시스템은 'AI Captain' 페르소나를 중심으로 정성적 데이터(Macro)와 정량적 데이터(Micro)를 결합하는 **Decoupled Data Pipeline** 구조를 채택하였습니다.

### **[Data Flow]**
1.  **Macro Analysis (Qualitative)**: Perplexity Pro → Email Automation → **GAS(Google Apps Script)** → **Google Sheets**.
2.  **Micro Analysis (Quantitative)**: **KIS REST API** (실시간 시세, 수급, 이평선) → Python Backend.
3.  **Strategy Engine (AI Captain)**:
    *   **Gemini 2.0 Flash**: 이종 데이터 전처리 및 데이터 무결성 검증.
    *   **Gemini 1.5 Pro**: 'AI Captain' 페르소나를 기반으로 최종 투자 전략(Signal, Action Plan) 수립.
4.  **Delivery**: **Discord Webhook**을 통한 구조화된 **Embed** 메시지 전송.

---

## 🛠 2. Tech Stack & Tools

### **Backend & APIs**
- **Language**: Python 3.10+
- **Finance API**: 한국투자증권 KIS Developers (REST API, WebSocket, OAuth 2.0)
- **AI Models**: Gemini 1.5 Pro (Strategy), Gemini 2.0 Flash (Processing)
- **Research**: Perplexity Pro (Web-based Research)

### **Infrastructure & DevOps**
- **Automation**: **GitHub Actions** (Scheduled Task Runner)
- **Data Bridge**: **Google Apps Script (GAS)** (Email-to-Sheet ETL)
- **Database**: **Google Sheets** (Lightweight Data Lake)
- **Communication**: **Discord API** (Notification & Interactive Bot)

---

## 📌 3. Project Roadmap & Milestones

### ✅ v0.1.0: Foundation (Completed)
- [x] 프로젝트 인프라 및 가상환경(venv) 구축.
- [x] **KIS OAuth 2.0 인증 모듈 (`auth.py`)**: 토큰 캐싱 로직 포함.
- [x] **Discord 알림 엔진 (`discord_bot.py`)**: Embed 카드 메시지 레이아웃 구현.
- [x] 보안 설정 완료 (`.env`, `.gitignore` - data/ 폴더 격리).

### 🟡 v0.2.0: Research ETL Pipeline (Next)
- [ ] GAS 기반 Gmail 뉴스 데이터 자동 파싱 및 Google Sheets 적재.
- [ ] Google Sheets API 연동 모듈 개발.

### 🟠 v0.3.0: Intelligence Strategy Engine
- [ ] 'AI Captain' 페르소나 주입 및 프롬프트 엔지니어링 최적화.
- [ ] KIS API 기반 기술적 지표 추출 모듈 통합.

### 🔴 v0.4.0: Tactical Real-time Mode
- [ ] **Async/WebSocket** 기반 실시간 데이터 스트리밍.
- [ ] **Interactive Discord Bot**: AI Captain과의 양방향 실시간 전략 대화 기능.

---

## 🔥 4. Engineering Challenges & Solutions

### ✅ 토큰 매니징 및 API 최적화 (v0.1.0 해결)
- **Problem**: 24시간마다 만료되는 증권사 토큰과 빈번한 API 호출로 인한 서버 부하.
- **Solution**: 로컬 파일 시스템을 활용한 **Token Caching 전략**을 수립하여 유효성 검증 후 필요 시에만 재발급받도록 구현.

### ✅ 'AI Captain' 분석 로직의 신뢰성 확보
- **Problem**: LLM의 환각 현상(Hallucination)으로 인한 잘못된 수치 판단 위험.
- **Solution**: 데이터 소스를 **Macro(Perplexity)**와 **Micro(KIS API)**로 엄격히 분리하고, 최종 판단 전 Gemini 2.0 Flash를 활용한 교차 검증 파이프라인 설계.

---

## 👨‍💻 5. Developer's Note
이 프로젝트는 기술적 구현을 넘어 **'데이터가 어떻게 비즈니스적 가치(Profit)를 창출하는가'**에 대한 고찰을 담고 있습니다. 모든 코드는 유지보수성과 확장성을 고려하여 클린 코드 원칙을 준수합니다.

---

## 📂 6. Directory Structure
```text
.
├── src/
│   ├── auth.py         # KIS API 인증 및 토큰 관리
│   └── discord_bot.py  # 디스코드 알림 및 Embed 포맷팅
├── data/               # 토큰 및 로컬 캐시 데이터 (Git 제외)
├── .env                # API 키 및 보안 환경 변수
├── .gitignore          # 보안 파일 및 가상환경 제외 설정
└── requirements.txt    # 프로젝트 의존성 관리
