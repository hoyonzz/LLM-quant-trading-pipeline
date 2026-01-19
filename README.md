# 📈 LLM-Quant Strategy Pipeline (LQSP)

> **"지능형 에이전트 기반의 데이터 통합 및 투자 전략 수립 자동화 파이프라인"**

본 프로젝트는 불확실성이 높은 금융 시장에서 개인 투자자의 감정적 편향을 배제하고, **LLM(Gemini 1.5 Pro)의 전략적 추론**과 **증권사 REST API의 정량 데이터**를 결합하여 수익을 창출하는 **Semi-Auto Trading 인프라**를 구축합니다.

---

## 🏛 1. System Architecture

본 시스템은 정성적 데이터(뉴스/리포트)와 정량적 데이터(시세/수급)를 상호 보완적으로 결합하는 **Decoupled Data Pipeline** 구조를 채택하였습니다.

### **[Data Flow]**
1.  **Research**: Perplexity Pro (Web) → Email Automation → **Gmail API/GAS** → **Google Sheets** (Data Lake).
2.  **Market Data**: **KIS REST API** (실시간 시세, 수급, 이평선) → Python Backend.
3.  **Core Engine**:
    *   **Gemini 2.0 Flash**: 이종 데이터 병합 및 데이터 정규화 (Context Builder).
    *   **Gemini 1.5 Pro**: 리스크 관리 프로토콜에 따른 최종 투자 전략 수립 (Strategist).
4.  **Communication**: **Discord Webhook/Bot**을 통한 인터랙티브 매매 시나리오 전송.

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

### 🟢 v0.1.0: Foundation (Current)
- 프로젝트 인프라 구축 및 보안 설정 (.env, .gitignore).
- 한국투자증권(KIS) OAuth 2.0 인증 및 토큰 매니저 개발.
- Discord Webhook 연동 기초.

### 🟡 v0.2.0: Research ETL Pipeline
- GAS(Google Apps Script) 기반 Perplexity 리서치 데이터 자동 파싱.
- Google Sheets API를 활용한 데이터 적재 시스템.

### 🟠 v0.3.0: Intelligence Strategy Engine
- Gemini 1.5 Pro 기반 투자 시나리오 생성 프롬프트 엔지니어링.
- KIS REST API 기반 기술적 지표(이평선, RSI 등) 계산 모듈 구축.

### 🔴 v0.4.0: Tactical Real-time Mode
- **WebSocket 연동**: 실시간 호가 및 체결 데이터 스트리밍 처리.
- **Interactive Discord Bot**: 실시간 상황에 대한 LLM 즉각 질의응답 기능 추가.
- **Event-Driven Alert**: 급등락 발생 시 긴급 리스크 관리 전략 자동 전송.

---

## 🔥 4. Engineering Challenges & Solutions

### ✅ **Challenge 1: 이종 데이터 통합 및 환각(Hallucination) 제어**
*   **Problem**: 비정형 뉴스 데이터와 정형 수치 데이터를 결합할 때 LLM이 수치를 왜곡할 위험성 존재.
*   **Solution**: **'Two-Step Prompting'** 전략 도입. Gemini 2.0 Flash가 데이터 무결성을 먼저 검증하고, 규격화된 Markdown Context를 생성하여 1.5 Pro의 판단 정밀도 향상.

### ✅ **Challenge 2: 비용 효율적인 서버리스 파이프라인 설계**
*   **Problem**: 유료 API(Perplexity) 및 고정 서버 비용 발생 부담.
*   **Solution**: **GAS(Google Apps Script)**와 **GitHub Actions**의 크론(Cron) 기능을 조합하여 인프라 비용 0원의 ETL 및 스케줄링 파이프라인 구축.

### ✅ **Challenge 3: 안정적인 API 인증 및 Rate Limit 관리**
*   **Problem**: 24시간 후 만료되는 OAuth 2.0 토큰 및 증권사 API의 초당 호출 제한 대응 필요.
*   **Solution**: 토큰 자동 갱신 로직 및 요청 간 동적 딜레이를 관리하는 **Request Scheduler** 모듈 구현.

---

## 👨‍💻 5. Developer's Note
이 프로젝트는 기술적 구현을 넘어 **'데이터가 어떻게 비즈니스적 가치(Profit)를 창출하는가'**에 대한 고찰을 담고 있습니다. 모든 코드는 유지보수성과 확장성을 고려하여 클린 코드 원칙을 준수합니다.
