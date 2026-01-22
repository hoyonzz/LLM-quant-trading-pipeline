---

# 📈 LLM-Quant Strategy Pipeline (LQSP)

> **"지능형 에이전트(AI Captain) 기반의 데이터 통합 및 투자 전략 수립 자동화 파이프라인"**

본 프로젝트는 금융 시장의 감정적 편향을 제거하기 위해 **LLM(Gemini 1.5 Pro)**의 전략적 사고와 **증권사/AI API의 정밀 데이터**를 결합하여 수익을 창출하는 **Semi-Auto Trading 인프라**입니다.

---

### 🏗 1. System Architecture (Data Flow 수정)

1. **Macro Analysis**: Perplexity API → Python → Google Sheets.
2. **Micro Analysis**: KIS REST API → Python.
3. **Strategy Engine**: Gemini 1.5 Pro (Context-aware reasoning).
4. **Interface (The Front-end)**: **Discord**
    - **Push**: AI Captain의 전략 및 긴급 알림을 사용자에게 전달.
    - **Interactive**: 사용자가 전략 확인 후 디스코드로 '승인' 명령 전달 시 최종 매매 프로세스 진행.

---

### 🛠 2. Tech Stack & Tools

### **Backend & APIs**
- **Language**: Python 3.10+
- **Finance API**: 한국투자증권 KIS Developers (REST API, WebSocket)
- **AI Models**: Gemini 1.5 Pro (Strategy Engine), Gemini 2.0 Flash (Data Preprocessing), Perplexity API (Real-time Research)

### **Interface & Communication (핵심)**
- **Discord Webhook**: 장전/장후 브리핑 및 실시간 긴급 알림 전송용.
- **Discord Bot API (discord.py)**: AI Captain과의 실시간 양방향 질의응답 및 매매 승인 인터페이스.

### **Infrastructure & DevOps**
- **Automation**: GitHub Actions (Scheduled Task Runner)
- **Database**: Google Sheets (Data Lake), Local JSON (State/Token Management)
- **Secret Management**: Python-dotenv (.env)

---

## 📌 3. Operational Schedule (KST)

AI Captain은 시장의 변곡점에 맞춰 하루 5회의 정기 브리핑 및 실시간 긴급 감시를 수행합니다.

- **08:45 [Market Open Readiness]**: 글로벌 증시 브리핑 및 당일 타겟 종목 집중 리서치.
- **10:00 [Morning Trend Scan]**: 개장 후 1시간 추세 및 초기 수급 확인, 전략 확정.
- **13:30 [Mid-day Strategy]**: 오후장 방향성 체크 및 포지션 유지 여부 판단.
- **15:20 [Closing Decision]**: 종가 매매 여부 결정 및 내일 대응 시나리오 수립.
- **16:30 [Daily Review]**: 당일 매매 복기 및 'State JSON' 업데이트(Context 요약).
- **REAL-TIME [Emergency]**: 3분 내 2% 이상 변동, 5분 평균 대비 5배 거래량 폭증, 손절가(SL) 터치 시 즉각 대응.

---

## 🚀 4. Project Roadmap & Milestones

### ✅ v0.1.0: Foundation (Completed)
- [x] KIS API 인증 모듈(`auth.py`) 및 토큰 캐싱 로직 구현.
- [x] Discord 알림 엔진(`discord_bot.py`) 및 Embed 레이아웃 구축.

### 🟡 v0.2.0: Advanced Data Pipeline (Current)
- [x] Perplexity API 기반 리서치 자동화 (`researcher.py`).
- [x] AI 주도 섹터 및 종목 발굴 엔진 (`scanner.py`).
- [ ] Google Sheets 권한 재설정 및 데이터 로깅 최적화.
- [ ] **Market Data 모듈**: 체결강도 및 호가 데이터 추출 로직 구현.

### 🟠 v0.3.0: Intelligence Strategy Engine
- [ ] **Captain Engine**: Gemini 1.5 Pro 연동 및 `chat_history` 관리자 구축.
- [ ] **State Manager**: 누적 투자 데이터 요약 및 기억 유지 로직 개발.

### 🔴 v0.4.0: Tactical Real-time Mode & Interactive Bot
- [ ] **Async Monitoring**: `asyncio` 기반 실시간 시세 감시 시스템.
- [ ] **Interactive Discord Bot**: 
    - 단순 Webhook을 넘어 **상시 대기형 봇(Bot)**으로 업그레이드.
    - AI Captain에게 "현재 한올바이오파마 상황 어때?"라고 질문 시 즉각 답변하는 기능.
    - 버튼(Button)이나 선택 메뉴(Select Menu)를 통한 **매매 최종 승인 인터페이스** 구현.

---

## 🔥 5. Engineering Challenges & Solutions

### ✅ **[Issue #1] 데이터 수집 아키텍처 최적화**
*   **Problem**: Email-GAS 방식의 정보 누락 및 낮은 정보 밀도.
*   **Solution**: **Perplexity API** 직접 연동으로 전환하여 Full-text 리서치 데이터 확보 및 시스템 단순화.

### ✅ **[Issue #2] 토큰 및 보안 관리**
*   **Problem**: 인증 토큰 만료 처리 및 보안 키 유출 위험.
*   **Solution**: 로컬 파일 시스템 기반 토큰 캐싱 및 `.gitignore`를 통한 엄격한 보안 관리 적용.

### ⚠️ **[Issue #3] 투자 연속성을 위한 Context 유지 전략**
*   **Problem**: LLM API의 Stateless 특성으로 인한 이전 전략 망각.
*   **Solution**: 매일 장 마감 후 핵심 데이터를 요약하여 `State JSON`에 보관하고, 이를 다음 날 프롬프트의 **'기초 기억'**으로 주입하는 프로세스 설계.

### ⚠️ **[Issue #4] 실시간 감시 시스템의 효율적 구현**
*   **Problem**: 일반 While 루프 사용 시 발생하는 Blocking 현상 및 리소스 낭비.
*   **Solution**: `asyncio` 또는 멀티스레딩 기반의 비동기 아키텍처를 도입하여 메인 파이프라인과 실시간 감시 엔진을 분리할 예정.

---

## 📂 6. Directory Structure
```text
.
├── src/
│   ├── auth.py          # KIS API 인증 및 토큰 매니저
│   ├── discord_bot.py   # 디스코드 알림 및 Embed 포맷팅
│   ├── gsheet_manager.py # Google Sheets 데이터 로깅/로드
│   ├── researcher.py     # Perplexity API 리서치 엔진
│   ├── scanner.py        # 주도 섹터 및 종목 발굴 모듈
│   ├── market_data.py    # KIS 시세/수급 데이터 수집 (v0.2.0)
│   └── captain_engine.py # Gemini 1.5 Pro 전략 수립 엔진 (v0.3.0)
├── data/                # 토큰, 채팅 이력, 상태 JSON (Git 제외)
├── google_key.json      # Google Cloud 서비스 계정 키 (Git 제외)
├── .env                 # API 키 및 계좌 환경 변수
└── .gitignore           # 보안 및 가상환경 제외 설정
```

---
