import os
from dotenv import load_dotenv
import logging

# .env 파일 로드 (프로젝트 루트에 있는 .env 파일)
# 스크립트 실행 위치에 따라 경로 조정 필요 시: load_dotenv(dotenv_path=find_dotenv())
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# 로깅 설정
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Kafka 설정
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'upbit-ticker-data')

# Upbit 설정
UPBIT_WEBSOCKET_URI = os.getenv('UPBIT_WEBSOCKET_URI', 'wss://api.upbit.com/websocket/v1')
MARKET_CODES_STR = os.getenv('MARKET_CODES', 'KRW-BTC')
MARKET_CODES = [code.strip().upper() for code in MARKET_CODES_STR.split(',')]

# 애플리케이션 설정
RECONNECT_DELAY_SECONDS = 5 # 웹소켓 재연결 시도 간격 (초)

# 설정값 로깅
logger.info("--- Application Configuration ---")
logger.info(f"KAFKA_BROKERS: {KAFKA_BROKERS}")
logger.info(f"KAFKA_TOPIC: {KAFKA_TOPIC}")
logger.info(f"UPBIT_WEBSOCKET_URI: {UPBIT_WEBSOCKET_URI}")
logger.info(f"MARKET_CODES: {MARKET_CODES}")
logger.info(f"RECONNECT_DELAY_SECONDS: {RECONNECT_DELAY_SECONDS}")
logger.info("-------------------------------")
