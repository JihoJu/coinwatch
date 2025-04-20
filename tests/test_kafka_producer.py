import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.kafka_producer import create_producer, send_to_kafka, stop_producer

@pytest.mark.asyncio
@patch('src.kafka_producer.AIOKafkaProducer')
async def test_create_producer_success(mock_producer_class):
    """Kafka 프로듀서 생성 성공 테스트"""
    # 설정 (arrange)
    mock_producer_instance = MagicMock()
    mock_producer_instance.start = AsyncMock()  # start 메서드만 AsyncMock으로 설정
    mock_producer_class.return_value = mock_producer_instance

    # 실행 (act)
    producer = await create_producer()

    # 검증 (assert)
    mock_producer_class.assert_called_once()
    assert mock_producer_instance.start.call_count == 1  # start가 한 번 호출되었는지 확인
    assert producer == mock_producer_instance

@pytest.mark.asyncio
@patch('src.kafka_producer.AIOKafkaProducer')
async def test_create_producer_failure(mock_producer_class):
    """Kafka 프로듀서 생성 실패 테스트"""
    # 설정 (arrange)
    mock_producer_instance = MagicMock()
    mock_producer_instance.start = AsyncMock(side_effect=Exception("Kafka connection error"))
    mock_producer_class.return_value = mock_producer_instance

    # 실행 (act)
    producer = await create_producer()

    # 검증 (assert)
    mock_producer_class.assert_called_once()
    assert mock_producer_instance.start.call_count == 1
    assert producer is None

@pytest.mark.asyncio
async def test_send_to_kafka_success():
    """Kafka 메시지 전송 성공 테스트"""
    # 설정 (arrange)
    mock_producer = MagicMock()
    
    # Future 객체 설정
    mock_record_metadata = MagicMock()
    mock_record_metadata.partition = 0
    mock_record_metadata.offset = 1
    
    async def mock_send(*args, **kwargs):
        return mock_record_metadata
    
    mock_producer.send = AsyncMock(side_effect=mock_send)

    topic = "test-topic"
    data = {
        "code": "KRW-BTC",
        "price": 50000000
    }

    # 실행 (act)
    await send_to_kafka(mock_producer, topic, data)

    # 검증 (assert)
    mock_producer.send.assert_called_once_with(
        topic,
        value=data,
        key=b'KRW-BTC'
    )

@pytest.mark.asyncio
async def test_stop_producer_success():
    """Kafka 프로듀서 정상 종료 테스트"""
    # 설정 (arrange)
    mock_producer = MagicMock()
    mock_producer.stop = AsyncMock()

    # 실행 (act)
    await stop_producer(mock_producer)

    # 검증 (assert)
    assert mock_producer.stop.call_count == 1

@pytest.mark.asyncio
async def test_stop_producer_failure():
    """Kafka 프로듀서 종료 실패 테스트"""
    # 설정 (arrange)
    mock_producer = MagicMock()
    mock_producer.stop = AsyncMock(side_effect=Exception("Stop error"))

    # 실행 (act)
    await stop_producer(mock_producer)

    # 검증 (assert)
    assert mock_producer.stop.call_count == 1