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

3.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **환경 변수 설정:**
    `.env` 파일을 생성하고 필요한 환경 변수 (예: Kafka 브로커 주소, 토픽 이름 등) 를 설정합니다. `.env.example` 파일이 있다면 참고하여 작성합니다.

5.  **실행:**
    ```bash
    python src/main.py
    ```

6.  **(테스트 시) DEBUG 레벨 로깅 활성화:**
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