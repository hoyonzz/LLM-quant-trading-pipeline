# 🚀 한국투자증권 REST API 완벽 가이드
## LQSP 백엔드 개발자 취업 준비용

---

## 📌 목차
1. [REST API란? (취업면접 대비)](#1-rest-api란-취업면접-대비)
2. [OAuth 2.0 인증 체계](#2-oauth-20-인증-체계)
3. [KIS API 주요 Endpoints 사전](#3-kis-api-주요-endpoints-사전)
4. [Python 구현 예제 (auth.py 샘플)](#4-python-구현-예제-authpy-샘플)
5. [Rate Limiting & Token Management](#5-rate-limiting--token-management)
6. [실전 코드 패턴](#6-실전-코드-패턴)

---

## 1. REST API란? (취업면접 대비)

### 📖 정의
**REST(Representational State Transfer)** 는 웹 아키텍처 스타일로, HTTP 프로토콜을 통해 서버-클라이언트 간 데이터를 주고받는 방식입니다.

### 🎯 REST의 핵심 원칙 (필수 암기)

| 원칙 | 설명 | 예시 |
|------|------|------|
| **HTTP Method** | 리소스 작업을 HTTP 메서드로 표현 | GET(조회), POST(생성), PUT(수정), DELETE(삭제) |
| **Resource** | 모든 것을 리소스(명사)로 표현 | `/stocks/005930` (삼성전자 종목) |
| **Stateless** | 각 요청이 완전하고 독립적 | 서버가 클라이언트 상태 저장하지 않음 |
| **Representation** | JSON/XML 형식으로 데이터 반환 | `{"price": 70000, "change": +500}` |

### 💼 면접 꿀팁
> **Q: REST API의 장점은?**
> - ✅ 표준화된 HTTP 프로토콜 사용 → 호환성 좋음
> - ✅ Stateless 설계 → 수평 확장 용이 (Scale-out)
> - ✅ 캐싱 활용 가능 → 성능 개선
> - ✅ 브라우저에서 직접 테스트 가능

### KIS API의 특징
```
✅ REST 방식 (OCX 없음) → 파이썬/자바/C# 등 모든 언어 지원
✅ OAuth 2.0 표준 인증
✅ JSON 응답 형식
✅ 24시간 운영 서버
```

---

## 2. OAuth 2.0 인증 체계

### 📊 OAuth 2.0 Flow (KIS 기준)

```
┌─────────────────────────────────────────────────────────┐
│                   KIS OAuth 2.0 Flow                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1️⃣ 앱 등록                                              │
│  └─> Client ID, Client Secret 발급                      │
│                                                          │
│  2️⃣ Access Token 발급 요청                              │
│  POST /oauth2/tokenP                                    │
│  ├─ grant_type: "client_credentials"                   │
│  ├─ client_id: "YOUR_CLIENT_ID"                        │
│  └─ client_secret: "YOUR_CLIENT_SECRET"                │
│                                                          │
│  3️⃣ Access Token 수신                                   │
│  ├─ access_token (유효기간: 24시간)                    │
│  └─ token_type: "Bearer"                               │
│                                                          │
│  4️⃣ API 요청 (Header에 Token 포함)                     │
│  GET /uapi/domestic-stock/v1/quotations/inquire-price  │
│  Authorization: Bearer {access_token}                  │
│  ├─ Content-Type: application/json                     │
│  ├─ custtype: P (Persona) / B (Business)              │
│  └─ tr-id: FHKST01010100 (트랜잭션 ID)               │
│                                                          │
│  5️⃣ 데이터 응답 (JSON)                                 │
│  └─ 시세/수급/계좌 정보 수신                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 🔑 주요 용어 정리

| 용어 | 의미 | 예시 |
|------|------|------|
| **Client ID** | API 사용자를 식별하는 고유 코드 | `abcd1234efgh5678` |
| **Client Secret** | 비밀번호 (절대 노출하면 안됨!) | `.env` 파일에 저장 |
| **Access Token** | API 호출 권한을 나타내는 인증 토큰 | `Bearer eyJhbGc...` |
| **Token Type** | 토큰 종류 (KIS는 항상 "Bearer") | `Bearer` |
| **Expires In** | 토큰 유효기간 (초 단위) | `86400` (24시간) |
| **Refresh Token** | (KIS는 미제공) 토큰 갱신용 | N/A |

### ⚠️ KIS OAuth 특이사항
- **2-legged OAuth**: 사용자 인증 불필요 (앱만 인증)
- **Token 갱신**: 6시간마다 새 토큰 발급 (캐싱 권장)
- **자동 갱신**: 토큰 만료 시 `InvalidTokenError` 발생 → 자동 재발급 필요

---

## 3. KIS API 주요 Endpoints 사전

### 📋 카테고리별 API 목록

#### **[1] 인증 관련**

| Endpoint | HTTP | 설명 | 필수 Parameter |
|----------|------|------|-----------------|
| `/oauth2/tokenP` | POST | 접근 토큰 발급 (Persona) | client_id, client_secret, grant_type |
| `/oauth2/tokenB` | POST | 접근 토큰 발급 (Business) | client_id, client_secret, grant_type |
| `/oauth2/revoke` | POST | 토큰 폐기 | access_token |

**사용 예시:**
```python
# 토큰 발급
POST https://openapi.koreainvestment.com:9443/oauth2/tokenP
{
    "grant_type": "client_credentials",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
}

# 응답
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400
}
```

---

#### **[2] 국내주식 현재가 조회 (핵심!)**

| Endpoint | HTTP | 설명 | 사용 빈도 |
|----------|------|------|----------|
| `/uapi/domestic-stock/v1/quotations/inquire-price` | GET | **종목 현재가 조회** | ⭐⭐⭐⭐⭐ |
| `/uapi/domestic-stock/v1/quotations/inquire-asking-price` | GET | 호가 조회 (Bid/Ask) | ⭐⭐⭐ |
| `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice` | GET | 일봉 차트 데이터 | ⭐⭐⭐⭐ |

**가장 많이 사용할 API: 현재가 조회**
```python
# Request
GET https://openapi.koreainvestment.com/uapi/domestic-stock/v1/quotations/inquire-price
Headers:
  - Authorization: Bearer {access_token}
  - Content-Type: application/json
  - custtype: P
  - tr-id: FHKST01010100

Query Parameters:
  - fid_cond_mrkt_div_code: J (국내) / N (해외)
  - fid_input_iscd: 005930 (삼성전자 종목코드)

# Response
{
    "rt_cd": "0",  // 0 = 성공, 그 외 = 에러
    "msg_cd": "0000000000",
    "msg1": "NORMAL",
    "output": {
        "mksc_shrn_iscd": "005930",
        "stck_prpr": "70500",  // 주식 현재가
        "prdy_vrss": "500",     // 전일 대비
        "prdy_vrss_sign": "5",  // 5=상승, 3=하락, 4=동결
        "prdy_ctrt": "0.71",    // 전일 대비 등락률
        "stck_oprc": "70000",   // 시가
        "stck_hgpr": "71000",   // 고가
        "stck_lwpr": "70000",   // 저가
        "cntg_vol": "5000000",  // 거래량
        "acml_vol": "30000000"  // 누적 거래량
    }
}
```

---

#### **[3] 국내주식 주문 (매매)**

| Endpoint | HTTP | 설명 | 위험도 |
|----------|------|------|--------|
| `/uapi/domestic-stock/v1/trading/order-cash` | POST | **현금 매수/매도** | 🔴 높음 |
| `/uapi/domestic-stock/v1/trading/order-change` | PUT | 주문 정정 | 🔴 높음 |
| `/uapi/domestic-stock/v1/trading/order-cancel` | DELETE | 주문 취소 | 🔴 높음 |

**매수 주문 예시 (실제 돈이 나간다!)**
```python
# Request
POST https://openapi.koreainvestment.com/uapi/domestic-stock/v1/trading/order-cash
Headers: [Authorization, Content-Type, custtype, tr-id, ...]

Body:
{
    "CANO": "12345678",          // 계좌번호
    "ACNT_PRDT_CD": "01",        // 계좌상품코드
    "PDNO": "005930",             // 종목코드 (삼성전자)
    "ORD_DVSN": "01",             // 01=시장가, 00=지정가
    "CBLC_TMN": "00000000",       // 신용기간
    "ORD_QTY": "10",              // 주문수량
    "ORD_UNPR": "70000"           // 주문단가 (지정가일 때만)
}

# Response
{
    "rt_cd": "0",
    "output": {
        "KRX_FWDNO": "000000000000",    // 선물번호
        "ODNO": "00123456789",          // 주문번호
        "ORD_TMD": "093000"             // 주문시각
    }
}
```

---

#### **[4] 계좌 조회**

| Endpoint | HTTP | 설명 | 필수 |
|----------|------|------|-----|
| `/uapi/domestic-stock/v1/trading/inquire-balance` | GET | **잔고 조회** | ✅ |
| `/uapi/domestic-stock/v1/trading/inquire-daily-ccld` | GET | 일별 주문체결 조회 | ✅ |
| `/uapi/domestic-stock/v1/trading/inquire-possible-buy` | GET | 매수 가능 금액 조회 | ⭐ |

**잔고 조회 (포트폴리오 확인)**
```python
# Request
GET https://openapi.koreainvestment.com/uapi/domestic-stock/v1/trading/inquire-balance
Query:
  - cano: 12345678
  - acnt_prdt_cd: 01
  - afhr_flpr_yn: N  // 시간외 단가 포함 여부
  - od_dvsn: 00      // 00=전체, 01=매수, 02=매도

# Response (보유 종목 리스트)
{
    "output1": [
        {
            "pdno": "005930",           // 종목코드
            "prdt_name": "삼성전자",
            "hldg_qty": "100",          // 보유수량
            "ord_psbl_qty": "100",      // 매도 가능수량
            "pchs_avg_pric": "70000",   // 매입 평균가
            "pchs_amt": "7000000",      // 매입금액
            "prpr": "70500",            // 현재가
            "evlu_amt": "7050000",      // 평가금액
            "evlu_pfls": "50000",       // 평가손익
            "evlu_pfls_rt": "0.71"      // 수익률
        }
    ],
    "output2": {
        "dnca_tot_amt": "10000000",    // 예수금
        "nxdy_excc_amt": "0",          // 다음일 인수금
        "asst_icamt": "17050000",      // 총자산
        "trad_dvsn": "00"              // 거래구분
    }
}
```

---

#### **[5] 실시간 데이터 (WebSocket)**

| Method | 설명 | 용도 |
|--------|------|------|
| **WebSocket** | 실시간 호가/체결 스트리밍 | 틱 데이터 수신 |
| `접속키 발급` | 웹소켓 연결용 임시 키 | 보안 인증 |

**실시간 호가 예시:**
```json
{
    "header": {
        "appkey": "YOUR_APP_KEY",
        "secretkey": "YOUR_SECRET",
        "custtype": "P",
        "tr_type": "1",
        "content-type": "utf-8"
    },
    "body": {
        "input": {
            "tr_id": "H0312",            // 실시간 호가 TR ID
            "tr_key": "005930"           // 종목코드
        }
    }
}
```

---

### 🔍 자주 사용할 TR ID (Transaction ID) 목록

| TR ID | 설명 | 호출 주기 |
|-------|------|---------|
| `FHKST01010100` | 현재가 조회 | 1초 |
| `TTTC0802R` | 실시간 호가 (웹소켓) | 실시간 |
| `TTTC0801R` | 실시간 체결 (웹소켓) | 실시간 |
| `FHKST10010000` | 일봉 차트 | 1분 |
| `VHKST01010000` | 일별 주문체결 | 1분 |

---

## 4. Python 구현 예제 (auth.py 샘플)

### ✅ 프로덕션 레벨 인증 모듈

```python
# auth.py
import os
import json
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, Optional

# .env 파일 로드
load_dotenv()

class KISAuthManager:
    """한국투자증권 OAuth 2.0 인증 및 토큰 관리"""
    
    def __init__(self):
        self.client_id = os.getenv("KIS_CLIENT_ID")
        self.client_secret = os.getenv("KIS_CLIENT_SECRET")
        self.app_key = os.getenv("KIS_APP_KEY")
        self.app_secret = os.getenv("KIS_APP_SECRET")
        self.custtype = "P"  # Persona
        
        # 토큰 캐싱
        self.access_token: Optional[str] = None
        self.token_issued_at: Optional[datetime] = None
        self.token_expiry: Optional[datetime] = None
        
        # API 기본 설정
        self.base_url_real = "https://openapi.koreainvestment.com"
        self.base_url_mock = "https://openapivirt.koreainvestment.com:29443"  # 모의 서버
        self.oauth_url = "https://openapi.koreainvestment.com:9443"
        
    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        접근 토큰 획득 (캐싱 및 자동 갱신)
        
        Args:
            force_refresh: True면 기존 토큰 무시하고 새로 발급
            
        Returns:
            access_token 문자열
        """
        # 캐시된 토큰이 유효한 경우 반환
        if self.access_token and not force_refresh:
            if self.token_expiry and datetime.now() < self.token_expiry - timedelta(minutes=5):
                print(f"✅ 캐시된 토큰 사용 (만료까지 {(self.token_expiry - datetime.now()).seconds}초)")
                return self.access_token
        
        # 새 토큰 발급
        print("🔄 새로운 Access Token 발급 중...")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(
                f"{self.oauth_url}/oauth2/tokenP",
                headers=headers,
                data=data,
                timeout=10,
                verify=True  # SSL 인증서 검증
            )
            response.raise_for_status()  # HTTP 에러 체크
            
            token_response = response.json()
            
            if "access_token" not in token_response:
                raise ValueError(f"토큰 발급 실패: {token_response}")
            
            self.access_token = token_response["access_token"]
            self.token_issued_at = datetime.now()
            self.token_expiry = datetime.now() + timedelta(seconds=token_response.get("expires_in", 86400))
            
            print(f"✅ 토큰 발급 완료 (유효기간: {token_response.get('expires_in')}초)")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 토큰 발급 실패: {e}")
            raise
    
    def revoke_token(self) -> bool:
        """토큰 폐기 (로그아웃)"""
        if not self.access_token:
            return False
        
        headers = {"Content-Type": "application/json"}
        data = {"access_token": self.access_token}
        
        try:
            response = requests.post(
                f"{self.oauth_url}/oauth2/revoke",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.access_token = None
                self.token_expiry = None
                print("✅ 토큰 폐기 완료")
                return True
            else:
                print(f"⚠️ 토큰 폐기 실패: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 토큰 폐기 오류: {e}")
            return False


class KISAPIClient:
    """한국투자증권 REST API 클라이언트"""
    
    def __init__(self, auth_manager: KISAuthManager, use_mock: bool = False):
        self.auth = auth_manager
        self.use_mock = use_mock
        self.base_url = auth_manager.base_url_mock if use_mock else auth_manager.base_url_real
        self.request_count = 0
        self.last_request_time = None
        
    def _get_headers(self) -> Dict:
        """API 요청용 헤더 생성"""
        token = self.auth.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "custtype": self.auth.custtype,
            "tr-id": "",  # 각 API마다 설정
        }
    
    def _rate_limit(self, delay: float = 0.1):
        """Rate Limit 관리 (초당 최대 요청 수 제한)"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < delay:
                time.sleep(delay - elapsed)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def inquire_price(self, fid_input_iscd: str) -> Dict:
        """
        현재가 조회
        
        Args:
            fid_input_iscd: 종목코드 (예: "005930" = 삼성전자)
            
        Returns:
            현재가 데이터
        """
        self._rate_limit()
        
        headers = self._get_headers()
        headers["tr-id"] = "FHKST01010100"
        
        params = {
            "fid_cond_mrkt_div_code": "J",  # 국내
            "fid_input_iscd": fid_input_iscd
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price",
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("rt_cd") != "0":
                raise ValueError(f"API 에러: {data.get('msg1')}")
            
            return data.get("output", {})
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 현재가 조회 실패: {e}")
            raise
    
    def inquire_balance(self, account_number: str, product_code: str = "01") -> Dict:
        """
        잔고 조회
        
        Args:
            account_number: 계좌번호 (예: "12345678")
            product_code: 계좌상품코드 (기본값: "01")
            
        Returns:
            보유 종목 및 자산 정보
        """
        self._rate_limit()
        
        headers = self._get_headers()
        headers["tr-id"] = "TTTC8434R"
        
        params = {
            "cano": account_number,
            "acnt_prdt_cd": product_code,
            "afhr_flpr_yn": "N",
            "od_dvsn": "00"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/uapi/domestic-stock/v1/trading/inquire-balance",
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("rt_cd") != "0":
                raise ValueError(f"API 에러: {data.get('msg1')}")
            
            return {
                "holdings": data.get("output1", []),
                "summary": data.get("output2", {})
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 잔고 조회 실패: {e}")
            raise


# ==================== 사용 예제 ====================

if __name__ == "__main__":
    # 1️⃣ 인증 초기화
    auth = KISAuthManager()
    
    # 2️⃣ API 클라이언트 생성 (모의 서버 테스트)
    client = KISAPIClient(auth, use_mock=True)
    
    # 3️⃣ 현재가 조회
    try:
        price_data = client.inquire_price("005930")  # 삼성전자
        print(f"\n삼성전자 현재가: {price_data['stck_prpr']}원")
        print(f"전일 대비: {price_data['prdy_vrss']:+.2f}({price_data['prdy_ctrt']:+.2f}%)")
    except Exception as e:
        print(f"에러: {e}")
    
    # 4️⃣ 잔고 조회
    try:
        balance = client.inquire_balance("12345678")
        print(f"\n보유 종목 수: {len(balance['holdings'])}")
        print(f"총자산: {balance['summary']['asst_icamt']}원")
    except Exception as e:
        print(f"에러: {e}")
    
    # 5️⃣ 종료 시 토큰 폐기
    auth.revoke_token()
```

### 🔧 .env 파일 (비밀정보 관리)

```env
# .env
# ⚠️ 절대 Github에 commit하지 말 것!

# KIS API 인증 정보
KIS_CLIENT_ID=your_client_id_here
KIS_CLIENT_SECRET=your_client_secret_here
KIS_APP_KEY=your_app_key_here
KIS_APP_SECRET=your_app_secret_here

# 계좌 정보 (선택)
KIS_ACCOUNT_NUMBER=12345678
KIS_PRODUCT_CODE=01

# 환경 설정
USE_MOCK_SERVER=False  # True면 모의 서버 사용
LOG_LEVEL=INFO
```

### 📦 requirements.txt

```
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## 5. Rate Limiting & Token Management

### ⚙️ Rate Limit 정책

| 구분 | 제한 | 대책 |
|------|------|------|
| **초당 요청** | 최대 10 req/sec | `time.sleep(0.1)` |
| **분당 요청** | 최대 600 req/min | 동적 조절 |
| **토큰 갱신** | 6시간마다 | 자동 갱신 로직 |

### 🛡️ 에러 처리 전략

```python
# error_handler.py

class KISAPIException(Exception):
    """KIS API 기본 예외"""
    pass

class TokenExpiredError(KISAPIException):
    """토큰 만료"""
    def __init__(self):
        super().__init__("Access Token 만료됨")

class RateLimitExceededError(KISAPIException):
    """Rate Limit 초과"""
    def __init__(self):
        super().__init__("Rate Limit 초과 - 요청 대기 필요")

class InvalidTokenError(KISAPIException):
    """유효하지 않은 토큰"""
    def __init__(self):
        super().__init__("유효하지 않은 토큰 - 재발급 필요")

# API 호출 with 재시도 로직
def api_call_with_retry(func, max_retries=3, backoff_factor=2):
    """지수 백오프를 사용한 재시도"""
    for attempt in range(max_retries):
        try:
            return func()
        except TokenExpiredError:
            print(f"🔄 토큰 재발급 (시도 {attempt+1}/{max_retries})")
            auth.get_access_token(force_refresh=True)
            if attempt == max_retries - 1:
                raise
        except RateLimitExceededError:
            wait_time = backoff_factor ** attempt
            print(f"⏱️ Rate Limit 대기 중... {wait_time}초")
            time.sleep(wait_time)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"⚠️ 요청 실패, 재시도 중... ({attempt+1}/{max_retries})")
            time.sleep(backoff_factor ** attempt)
```

---

## 6. 실전 코드 패턴

### 📊 패턴 1: 여러 종목의 현재가 배치 조회

```python
def get_multiple_prices(symbols: list[str]) -> Dict[str, Dict]:
    """여러 종목 현재가 동시 조회 (병렬처리)"""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 최대 5개 스레드로 병렬 요청
        futures = {
            executor.submit(client.inquire_price, sym): sym 
            for sym in symbols
        }
        
        for future in as_completed(futures):
            sym = futures[future]
            try:
                results[sym] = future.result()
                print(f"✅ {sym} 조회 완료")
            except Exception as e:
                print(f"❌ {sym} 조회 실패: {e}")
                results[sym] = None
    
    return results

# 사용
symbols = ["005930", "000660", "051910"]  # 삼성전자, SK하이닉스, LG화학
prices = get_multiple_prices(symbols)
```

### 🤖 패턴 2: 정기적 모니터링 (Scheduler)

```python
from apscheduler.schedulers.background import BackgroundScheduler

def scheduled_monitoring():
    """매일 09:00~15:30에 5분마다 실행"""
    
    scheduler = BackgroundScheduler()
    
    def market_check():
        try:
            price = client.inquire_price("005930")
            print(f"[{datetime.now()}] 삼성전자: {price['stck_prpr']}원")
            # Discord 알림 발송
            send_discord_notification(f"삼성전자: {price['stck_prpr']}원")
        except Exception as e:
            print(f"모니터링 오류: {e}")
    
    # 평일 09:00~15:30, 5분마다 실행
    scheduler.add_job(
        market_check,
        'cron',
        day_of_week='0-4',  # 월~금
        hour='9-15',
        minute='*/5',
        second='0'
    )
    
    scheduler.start()
    print("📊 모니터링 시작!")

if __name__ == "__main__":
    scheduled_monitoring()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("종료")
```

### 💾 패턴 3: 데이터 파이프라인 (Google Sheets 연동)

```python
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import gspread

class DataPipeline:
    """KIS API → Google Sheets 자동 파이프라인"""
    
    def __init__(self, credentials_path: str):
        creds = Credentials.from_service_account_file(credentials_path)
        self.gc = gspread.authorize(creds)
        self.worksheet = self.gc.open("LQSP_Data").sheet1
    
    def update_price_data(self, symbols: list[str]):
        """현재가 데이터를 Google Sheets에 업로드"""
        prices = get_multiple_prices(symbols)
        
        # 헤더 설정
        self.worksheet.update_cell(1, 1, "종목코드")
        self.worksheet.update_cell(1, 2, "현재가")
        self.worksheet.update_cell(1, 3, "전일대비")
        self.worksheet.update_cell(1, 4, "수익률")
        self.worksheet.update_cell(1, 5, "업데이트시간")
        
        # 데이터 입력
        for idx, (sym, data) in enumerate(prices.items(), start=2):
            if data:
                self.worksheet.update_cell(idx, 1, sym)
                self.worksheet.update_cell(idx, 2, data['stck_prpr'])
                self.worksheet.update_cell(idx, 3, data['prdy_vrss'])
                self.worksheet.update_cell(idx, 4, data['prdy_ctrt'])
                self.worksheet.update_cell(idx, 5, datetime.now().isoformat())
        
        print(f"✅ {len(prices)}개 종목 데이터 업로드 완료")

# 사용
pipeline = DataPipeline("./credentials.json")
pipeline.update_price_data(["005930", "000660"])
```

---

## 🎓 면접 대비 핵심 포인트

### Q1: REST API와 SOAP의 차이점?
**A:** 
- REST: HTTP 기반, JSON/XML, 가벼움, 캐싱 가능 ✅
- SOAP: XML 기반, 복잡함, 상태 유지, 보안 강함

### Q2: OAuth 2.0에서 왜 토큰을 캐싱하나?
**A:** 매번 새로 발급하면 API 호출 지연 증가 → 응답시간 악화 → 매 요청마다 불필요한 인증 오버헤드

### Q3: Rate Limit을 초과하면?
**A:** 429 Too Many Requests 응답 → 지수 백오프(exponential backoff) 또는 대기열 사용

### Q4: Token Refresh vs Reauth?
**A:**
- Refresh: 만료 전 미리 갱신 (권장) → 사용자 경험 좋음
- Reauth: 만료 후 재인증 → 사용자 불편

---

## 📚 추가 학습 자료

1. **공식 문서**: https://apiportal.koreainvestment.com
2. **GitHub 샘플**: https://github.com/telemoon/-open-trading-api
3. **파이썬 래퍼**: https://github.com/Soju06/python-kis

---

## 체크리스트 ✅

- [ ] KIS 개발자센터 가입 및 API 신청 완료
- [ ] Client ID, Client Secret 안전하게 보관 (.env 파일)
- [ ] OAuth 2.0 토큰 발급 테스트 완료
- [ ] 현재가 조회 API 호출 성공
- [ ] 에러 처리 및 재시도 로직 구현
- [ ] Rate Limiting 적용
- [ ] Discord Webhook 연동
- [ ] GitHub Actions 스케줄링 설정

**화이팅! 🚀**
