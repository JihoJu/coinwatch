import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.upbit_ws_client import _process_message # 메시지 처리 로직 함수 이름으로 변경
from freezegun import freeze_time

@pytest.mark.asyncio
# expected_kafka_message에 있는 시간으로 고정
@freeze_time("2025-04-20T06:30:56.726492+00:00")
# kafka_producer 모듈에서 가져온 send_to_kafka 함수를 Mocking
@patch('src.upbit_ws_client.send_to_kafka', new_callable=AsyncMock)
async def test_process_ticker_message(mock_send_to_kafka):
    """Upbit Ticker 웹소켓 메시지 처리 성공 테스트"""
    # 설정 (arrange)
    # 실제 Upbit 에서 받는 것과 유사한 샘플 메시지 데이터 (JSON 혹은 dict)
    
    sample_message_data = b'{"type":"ticker","code":"KRW-BTC","opening_price":122720000.00000000,"high_price":123135000.00000000,"low_price":122677000.00000000,"trade_price":122902000.00000000,"prev_closing_price":122720000.00000000,"acc_trade_price":19699800600.2538100000000000,"change":"RISE","change_price":182000.00000000,"signed_change_price":182000.00000000,"change_rate":0.0014830508,"signed_change_rate":0.0014830508,"ask_bid":"ASK","trade_volume":0.00020372,"acc_trade_volume":160.18173252,"trade_date":"20250420","trade_time":"063055","trade_timestamp":1745130655618,"acc_ask_volume":80.07639388,"acc_bid_volume":80.10533864,"highest_52_week_price":163325000.00000000,"highest_52_week_date":"2025-01-20","lowest_52_week_price":72100000.00000000,"lowest_52_week_date":"2024-08-05","market_state":"ACTIVE","is_trading_suspended":false,"delisting_date":null,"market_warning":"NONE","timestamp":1745130655652,"acc_trade_price_24h":67648718116.20854000,"acc_trade_volume_24h":549.81614150,"stream_type":"SNAPSHOT"}'
    
    mock_kafka_producer = MagicMock() # Kafka 프로듀서 Mock 객체

    # 기대되는 결과 (Kafka 로 전송될 메시지 형태)
    expected_kafka_message = {
        'type': 'ticker', 
        'code': 'KRW-BTC', 
        'opening_price': 122720000.0, 
        'high_price': 123135000.0, 
        'low_price': 122677000.0, 
        'trade_price': 122902000.0, 
        'prev_closing_price': 122720000.0, 
        'acc_trade_price': 19699800600.25381, 
        'change': 'RISE', 
        'change_price': 182000.0, 
        'signed_change_price': 182000.0, 
        'change_rate': 0.0014830508, 
        'signed_change_rate': 0.0014830508, 
        'ask_bid': 'ASK', 
        'trade_volume': 0.00020372, 
        'acc_trade_volume': 160.18173252, 
        'trade_date': '20250420', 
        'trade_time': '063055', 
        'trade_timestamp': 1745130655618, 
        'acc_ask_volume': 80.07639388, 
        'acc_bid_volume': 80.10533864, 
        'highest_52_week_price': 163325000.0, 
        'highest_52_week_date': '2025-01-20', 
        'lowest_52_week_price': 72100000.0, 
        'lowest_52_week_date': '2024-08-05', 
        'market_state': 'ACTIVE', 
        'is_trading_suspended': False, 
        'delisting_date': None, 
        'market_warning': 'NONE', 
        'timestamp': 1745130655652, 
        'acc_trade_price_24h': 67648718116.20854, 
        'acc_trade_volume_24h': 549.8161415, 
        'stream_type': 'SNAPSHOT', 
        'received_timestamp_utc': '2025-04-20T06:30:56.726492+00:00'}
    
    kafka_topic = "upbit-ticker-data" # 실제 사용하는 토픽 이름

    # 실행 (act)
    await _process_message(sample_message_data, mock_kafka_producer, kafka_topic)

    # 검증 (assert)
    # send_to_kafka 함수가 올바른 인수로 호출되었는지 확인
    mock_send_to_kafka.assert_awaited_once_with(mock_kafka_producer, kafka_topic, expected_kafka_message)

# TODO: 다른 종류의 메시지 처리 테스트 (trade, orderbook 등)
# TODO: 잘못된 형식의 메시지 처리 테스트 (예외 처리, 로그 기록 등)
# TODO: 메시지 필터링 로직 테스트 (예: 특정 code 만 처리)
