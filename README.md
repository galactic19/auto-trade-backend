
# 자동매매 백엔드 시스템 (Auto-Trade Backend)

이 프로젝트는 주식 또는 가상자산의 자동매매를 위한 Django 기반 백엔드 API 서버입니다. 사용자 관리, 주문 실행, 대시보드, 랭킹 등의 기능을 제공합니다.

## ✨ 주요 기능

- **사용자 관리**: 회원가입, 로그인, JWT/토큰 기반 인증
- **주문 관리**: 지정가/시장가 매수 및 매도, 주문 수정 및 취소
- **대시보드**: 계좌 잔고, 수익률 등 거래 관련 데이터 시각화
- **랭킹 시스템**: 사용자별 수익률 또는 거래량 순위 제공
- **외부 거래 API 연동**: 키움증권 REST API와 연동하여 실제 거래 실행

## 📂 프로젝트 구조

```
D:/dev/auto-trade/backend/
├───.env                 # 환경 변수 설정 파일
├───manage.py             # Django 관리 스크립트
├───trade_config/         # 프로젝트 메인 설정
│   ├───settings.py       # Django 설정
│   └───urls.py           # 메인 URL 라우팅
├───accounts/             # 사용자 계정 및 인증 앱
├───dashboard/            # 대시보드 앱
├───order/                # 주문 관리 앱 (매수/매도)
├───rank/                 # 랭킹 관리 앱
└───utils/                # 공통 유틸리티 모듈
    └───tr_request.py     # 외부 API 요청 처리
```

- **trade_config**: Django 프로젝트의 메인 설정 파일과 전체 URL 라우팅을 관리합니다.
- **accounts**: 사용자 인증, 회원가입, 토큰 발급 등 계정 관련 기능을 담당합니다.
- **order**: 매수, 매도, 주문 조회/수정 등 거래 주문 관련 API를 담당합니다. 키움증권 REST API와 연동하여 실제 거래를 실행합니다.
- **dashboard**: 계좌 정보, 거래 내역 등 요약 정보를 제공하는 API를 담당합니다.
- **rank**: 사용자나 거래 성과에 대한 순위 관련 기능을 담당합니다.
- **utils**: 여러 앱에서 공통으로 사용하는 함수 (e.g., 외부 API 요청)를 포함합니다.

## 🚀 설치 및 실행 방법

### 1. 소스 코드 복제
```bash
git clone [저장소 URL]
cd backend
```

### 2. 가상 환경 생성 및 활성화
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. 필요 라이브러리 설치
`requirements.txt` 파일이 있다면 해당 파일을 사용하고, 없다면 아래 라이브러리를 설치합니다.
```bash
pip install django djangorestframework python-dotenv
```

### 4. 환경 변수 설정
루트 디렉토리에 `.env` 파일을 생성하고 아래 내용을 참고하여 환경 변수를 설정합니다.

```
# Django 설정
SECRET_KEY='django-insecure-your-secret-key'
DEBUG=True

# 거래 API 도메인 설정
KIWOOM_DOMAIN='https://openapi.kiwoom.com'  # 키움증권 실제 거래 API
MOTOO_DOMAIN='http://your-mock-api-server'  # 모의 거래 테스트용
```

### 5. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

### 6. 관리자 계정 생성 (선택 사항)
```bash
python manage.py createsuperuser
```

### 7. 개발 서버 실행
```bash
python manage.py runserver
```
서버가 실행되면 `http://127.0.0.1:8000/` 주소로 접속할 수 있습니다.

## ⚙️ API 사용법

### 기본 API 경로
- API의 기본 경로는 `http://127.0.0.1:8000/api/v1/` 입니다.

### 주요 엔드포인트
- **계정 관리**: `/api/v1/accounts/`
  - 토큰 발급: `GET /api/v1/accounts/` 또는 `/api/v1/accounts/me/`
  - 토큰 삭제: `DELETE /api/v1/accounts/delete/`
  - 계좌 정보: `GET /api/v1/accounts/account/`
  - 계좌 상세: `GET /api/v1/accounts/account/detail/`
- **주문 관리**: `/api/v1/order/`
  - 주식 매수: `POST /api/v1/order/buy/`
- **대시보드**: `/api/v1/dashboard/`
- **랭킹**: `/api/v1/rank/`

### 인증 방식
- 대부분의 API는 인증이 필요하며, 로그인 API를 통해 발급받은 토큰을 HTTP 요청 헤더에 `Authorization: Bearer [your_token]` 형식으로 포함하여 전송해야 합니다.
