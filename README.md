# Coinwatch

## 개요

본 프로젝트는 Upbit 거래소의 웹소켓 API를 이용하여 KRW-BTC 페어의 실시간 가격 및 거래량 데이터를 수집하고, 이를 Apache Kafka 토픽에 적재하는 시스템입니다.

## 주요 기능

- Upbit 웹소켓 API 연동
- KRW-BTC 실시간 시세 데이터 수집 (가격, 거래량)
- Kafka 토픽으로 데이터 전송

## 향후 계획

- BTC 외에 이더리움(ETH) 등 다른 암호화폐 데이터 수집 기능 추가

## 설치 및 실행 방법

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/JihoJu/coinwatch.git
    cd coinwatch
    ```

2.  **가상 환경 생성 및 활성화 (권장):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```

3. **프로젝트 설치:**
   ```bash
   pip install -e .
   ```
   이 명령어는 프로젝트를 개발 모드로 설치하며, 필요한 모든 의존성을 자동으로 설치합니다.

4. **환경 변수 설정:**
   `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다. `.env.example` 파일을 참고하여 작성합니다.
   ```bash
   cp .env.example .env
   # .env 파일을 편집하여 필요한 설정을 입력합니다.
   ```

5.  **실행:**
    ```bash
    python src/main.py
    ```

## 개발 환경 설정

### 프로젝트 구조

coinwatch/
├── src/
│ ├── init.py
│ ├── main.py
│ ├── config.py
│ ├── kafka_producer.py
│ └── upbit_ws_client.py
├── tests/
│ ├── init.py
│ ├── test_kafka_producer.py
│ └── test_upbit_ws_client.py
├── setup.py
├── requirements.txt
├── .env.example
└── README.md

### 의존성 관리
- 프로젝트는 `setup.py`를 통해 패키지로 관리됩니다.
- 개발을 위한 모든 의존성은 `pip install -e .` 명령으로 설치됩니다.
- 추가 의존성이 필요한 경우 `setup.py`의 `install_requires` 항목을 수정하세요.

### 로깅 설정
**(테스트 시) DEBUG 레벨 로깅 활성화:**
환경 변수 `LOG_LEVEL`을 `DEBUG`로 설정하여 실행하면 DEBUG 레벨 로그를 확인할 수 있습니다.

```bash
# Linux/macOS
export LOG_LEVEL=DEBUG
python src/main.py

# Windows (Command Prompt)
set LOG_LEVEL=DEBUG
python src/main.py

# Windows (PowerShell)
$env:LOG_LEVEL = "DEBUG"
python src/main.py
```
기본 로그 레벨은 `INFO` 입니다.

## 테스트

본 프로젝트는 pytest를 사용하여 단위 테스트를 구현하고 있습니다.

### 테스트 실행 방법

1. **전체 테스트 실행:**
   ```bash
   pytest
   ```

2. **특정 테스트 파일 실행:**
   ```bash
   pytest tests/test_kafka_producer.py
   pytest tests/test_upbit_ws_client.py
   ```

3. **특정 테스트 케이스 실행:**
   ```bash
   pytest tests/test_kafka_producer.py::test_create_producer_success
   ```

### 테스트 구성

- **Kafka 프로듀서 테스트** (`test_kafka_producer.py`):
  - 프로듀서 생성/종료 테스트
  - 메시지 전송 테스트
  - 예외 처리 테스트

- **Upbit 웹소켓 클라이언트 테스트** (`test_upbit_ws_client.py`):
  - 메시지 처리 로직 테스트
  - 웹소켓 연결 및 구독 테스트

### 테스트 환경 설정

테스트를 위한 의존성은 `requirements.txt`에 포함되어 있으며, 다음 패키지들이 사용됩니다:
- pytest
- pytest-asyncio (비동기 테스트용)
- freezegun (시간 관련 테스트용)