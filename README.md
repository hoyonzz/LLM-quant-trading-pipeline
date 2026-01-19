# 📈 LLM-Driven Investment Strategy Pipeline

> **AI 리서치와 실시간 금융 데이터를 결합한 지능형 투자 전략 수립 및 자동화 시스템**

본 프로젝트는 불확실성이 높은 주식 시장에서 **LLM(Large Language Model)**의 추론 능력과 **증권사 REST API**의 정밀 데이터를 결합하여, 감정에 휘둘리지 않는 객감적인 투자 전략을 수립하고 모니터링하는 백엔드 파이프라인입니다.

---

## 🏗 System Architecture

본 시스템은 데이터의 신뢰성을 확보하고 LLM의 환각(Hallucination)을 제어하기 위해 **Multi-Agent 구조**를 지향합니다.

1.  **Data Layer**: 
    *   **KIS(한국투자증권) API**: 실시간 시세, 수급(외인/기관), 이동평균선 등 정량 데이터 추출.
    *   **Perplexity AI**: 글로벌 거시 경제 지표 및 종목별 임상/이슈 등 정성 데이터 수집.
2.  **Processing Layer (Gemini 2.0 Flash)**: 
    *   이종 데이터(JSON, Text)를 정규화하고 전략 수립에 최적화된 Context로 변환.
3.  **Strategy Layer (Gemini 1.5 Pro)**: 
    *   사전에 정의된 **Risk Management Protocol**에 따라 최종 매매 시나리오 산출.
4.  **Delivery Layer (Discord)**: 
    *   Webhook을 통한 실시간 전략 보고서 및 변동성 알림 전송.

---

## 🛠 Tech Stack & Tools

- **Language**: Python 3.10+
- **Finance API**: KIS Developers (REST API, OAuth 2.0)
- **AI Models**: Gemini 1.5 Pro / 2.0 Flash, Perplexity API
- **Communication**: Discord Webhook
- **DevOps**: Environment Variable Management (dotenv), GitHub Actions (Scheduled Task)

---

## 🔥 Key Challenges & Solutions (Senior's Perspective)

### 1. LLM 환각 현상 및 데이터 신뢰성 확보
*   **Problem**: LLM이 잘못된 주가나 수치를 생성하여 의사결정에 치명적인 오류를 범할 위험이 있음.
*   **Solution**: 모든 수치 데이터는 증권사 API를 통해 수집된 데이터만 사용하도록 프롬프트를 설계하고, LLM은 '분석'과 '판단'의 역할만 수행하도록 역할을 분리(Decoupling).

### 2. 효율적인 API 인증 처리 및 Rate Limit 대응
*   **Problem**: 증권사 API의 접근 토큰(Access Token) 만료 및 초당 호출 제한 문제.
*   **Solution**: 토큰 갱신 로직을 자동화하고, 데이터 요청 간의 딜레이를 관리하는 스케줄러를 도입하여 시스템 안정성 확보.

### 3. 리스크 관리 프로토콜 구현
*   **Approach**: 단순 익절/손절가를 넘어, 시장 변동성(VIX)과 파트너사(IMVT 등)의 동향을 반영한 가변적 리스크 관리 로직을 파이프라인에 이식.

---

## 📋 Roadmap & Progress

- [ ] **Phase 1: Infra Setup**
    - [ ] 한국투자증권 API 연동 및 OAuth2 인증 모듈 개발
    - [ ] Discord Webhook 연동 및 포맷팅 엔진 구축
- [ ] **Phase 2: Data Pipeline**
    - [ ] Perplexity 기반 실시간 뉴스 스캐너 구현
    - [ ] 시세/수급 데이터 전처리 파이프라인 구축
- [ ] **Phase 3: Strategy Engine**
    - [ ] Gemini 1.5 Pro 기반 투자 전략 프롬프트 엔지니어링
    - [ ] 백테스팅 시뮬레이션 환경 구축
- [ ] **Phase 4: Optimization**
    - [ ] GitHub Actions를 이용한 파이프라인 자동화 실행
    - [ ] 다중 종목 확장성 테스트

---

## 👨‍💻 Developer's Note
이 프로젝트는 기술적 구현을 넘어 **'데이터가 어떻게 비즈니스적 가치(Profit)를 창출하는가'**에 대한 고찰을 담고 있습니다. 모든 코드는 유지보수성과 확장성을 고려하여 클린 코드 원칙을 준수하고자 노력했습니다.
