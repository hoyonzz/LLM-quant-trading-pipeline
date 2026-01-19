# 📈 LLM-Quant Strategy Pipeline (LQSP)

> **"지능형 에이전트 기반의 데이터 통합 및 투자 전략 수립 자동화 파이프라인"**

본 프로젝트는 불확실성이 높은 금융 시장에서 개인 투자자의 감정적 편향을 배제하고, **LLM(Gemini 1.5 Pro)의 전략적 추론**과 **증권사 REST API의 정량 데이터**를 결합하여 수익을 창출하는 **Semi-Auto Trading 인프라**를 구축합니다.

---

## 🏗 1. System Architecture

본 시스템은 정성적 데이터(뉴스/리포트)와 정량적 데이터(시세/수급)를 상호 보완적으로 결합하는 **Decoupled Data Pipeline** 구조를 채택하였습니다.

### **[Data Flow]**
1.  **Research**: Perplexity Pro (Web) → Email Automation → **Gmail API/GAS** → **Google Sheets** (Data Lake).
2.  **Market Data**: **KIS REST API** (실시간 시세, 수급, 이평선) → Python Backend.
3.  **Core Engine**:
    *   **Gemini 2.0 Flash**: 이종 데이터 병합 및 데이터 정규화 (Context Builder).
    *   **Gemini 1.5 Pro**: 리스크 관리 프로토콜에 따른 최종 투자 전략 수립 (Strategist).
4.  **Communication**: **Discord Webhook**을 통한 인터랙티브 매매 시나리오 전송.

---

## 🛠 2. Tech Stack & Tools

### **Backend & APIs**
- **Language**: Python 3.10+
- **Finance API**: 한국투자증권 KIS Developers (REST API, OAuth 2.0)
- **AI Models**: Gemini 1.5 Pro (Strategy), Gemini 2.0 Flash (Processing)
- **Research**: Perplexity Pro (Web-based Research)

### **Infrastructure & DevOps**
- **Automation**: **GitHub Actions** (Scheduled Task Runner)
- **Data Bridge**: **Google Apps Script (GAS)** (Email-to-Sheet ETL)
- **Database**: **Google Sheets** (Lightweight Data Lake)
- **Secret Management**: Python-dotenv (.env)

### **Communication**
- **Notification**: **Discord Webhook** (시각화된 전략 보고서 전송)

---

## 🔥 3. Engineering Challenges & Solutions

### ✅ **Challenge 1: 이종 데이터의 통합 및 환각(Hallucination) 제어**
*   **Problem**: Perplexity의 뉴스 데이터(비정형)와 KIS API의 수치 데이터(정형)를 결합할 때, LLM이 수치를 왜곡하거나 잘못된 근거를 생성할 위험이 있음.
*   **Solution**: **'Two-Step Prompting'** 전략 도입. 
    1. **Gemini 2.0 Flash**가 수치 데이터를 검증 및 마크다운 테이블로 규격화.
    2. **Gemini 1.5 Pro**는 규격화된 데이터만을 참조하여 전략을 수립하도록 제약을 설정하여 데이터 무결성 확보.

### ✅ **Challenge 2: API 비용 최적화 및 서버리스 파이프라인 구축**
*   **Problem**: 24시간 서버를 가동하거나 유료 AI API(Perplexity API)를 상시 호출하는 것은 비용 효율성이 낮음.
*   **Solution**: **GAS(Google Apps Script)**를 활용해 Perplexity의 무료 이메일 보고서를 파싱하고 Google Sheets에 적재하는 **Zero-Cost ETL** 프로세스 구축. 이후 **GitHub Actions**의 크론(Cron) 기능을 사용하여 서버 비용 없이 특정 시간(장전/장후)에만 파이프라인이 구동되도록 설계.

### ✅ **Challenge 3: 안정적인 API 인증 및 Rate Limit 관리**
*   **Problem**: 증권사 API의 OAuth 2.0 토큰은 24시간 후 만료되며, 초당 요청 제한(Rate Limit) 존재.
*   **Solution**: `auth.py` 모듈 내에 **토큰 캐싱 및 자동 갱신 로직**을 구현하고, API 호출 간 `time.sleep`을 동적으로 관리하는 **Request Scheduler**를 도입하여 시스템 중단 방지.

---

## 📋 4. Roadmap & Progress

- [ ] **Phase 1: Foundation Setup**
    - [ ] 한국투자증권 API OAuth2 인증 및 토큰 관리 모듈 (`auth.py`) 개발
    - [ ] Discord Webhook 포맷팅 엔진 구축
- [ ] **Phase 2: Data Pipe-lining**
    - [ ] GAS 기반 Gmail 뉴스 데이터 파싱 및 Google Sheets 적재 자동화
    - [ ] KIS API 기반 기술적 지표(이평선, 수급) 추출 스크립트 완성
- [ ] **Phase 3: Intelligence Layer**
    - [ ] Gemini 1.5 Pro 기반 투자 전략 프롬프트 엔지니어링 (Risk Management 포함)
    - [ ] 데이터 정규화 모듈 (Flash 모델 활용) 구축
- [ ] **Phase 4: Deployment**
    - [ ] GitHub Actions를 이용한 전체 파이프라인 스케줄링 완료
    - [ ] 트레이딩 로그 기록 및 전략 복기 시스템 구축

---

## 👨‍💻 5. Developer's Note
본 프로젝트는 백엔드 개발자로서 **"데이터의 수집-정제-가공-전달"**이라는 전체 생명 주기를 어떻게 효율적으로 관리할 것인가에 대한 고민을 담고 있습니다. 특히, 최신 LLM 기술을 비즈니스 로직(투자)에 안정적으로 통합하기 위한 **아키텍처 설계 역량**을 중점적으로 다루었습니다.

---
