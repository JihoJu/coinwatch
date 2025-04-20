import asyncio
import signal

from src.config import logger
from src.upbit_ws_client import upbit_websocket_client
from src.kafka_producer import create_producer, stop_producer

# 종료 신호 처리를 위한 플래그
shutdown_requested = False

def handle_shutdown_signal(sig, frame):
    """종료 신호(SIGINT, SIGTERM)를 처리합니다."""
    global shutdown_requested
    logger.info(f"Received shutdown signal: {sig}. Initiating graceful shutdown...")
    shutdown_requested = True

async def main():
    """애플리케이션 메인 실행 함수"""
    # Kafka 프로듀서 생성 및 시작
    producer = await create_producer()
    if not producer:
        logger.error("Failed to initialize Kafka producer. Exiting application.")
        return # 프로듀서 시작 실패 시 종료

    # 웹소켓 클라이언트 태스크 생성
    websocket_task = asyncio.create_task(upbit_websocket_client(producer))
    # 종료 신호 대기
    while not shutdown_requested:
        # 태스크가 예외로 종료되었는지 확인
        if websocket_task.done() and not websocket_task.cancelled():
            # 태스크가 정상적으로 완료된 경우 (취소되지 않고 완료됨)
            try:
                # 태스크 결과 확인 시 예외 발생 여부 확인 가능
                result = websocket_task.result()
                logger.info(f"WebSocket client task result: {result}")
            except Exception as e:
                logger.error(f"WebSocket client task exited unexpectedly: {e}")
                # 태스크가 예외로 종료된 경우
                # TODO: 여기서 애플리케이션 종료 또는 재시작 로직 구현 필요
                break # 예외 발생 시 메인 루프 종료

        await asyncio.sleep(1) # CPU 사용량 줄이기 위해 잠시 대기

    # 종료 절차 시작
    logger.info("Starting graceful shutdown...")

    # 웹소켓 태스크 취소 (진행 중인 작업 완료 기다리지 않고 즉시 중단 요청)
    if websocket_task and not websocket_task.done():
        websocket_task.cancel()
        try:
            await websocket_task # 취소가 완료될 때까지 대기
        except asyncio.CancelledError:
            logger.info("WebSocket client task successfully cancelled.")
        except Exception as e:
             logger.error(f"Error during WebSocket task cancellation: {e}")

    # Kafka 프로듀서 종료 (버퍼에 남은 메시지 전송 시도)
    await stop_producer(producer)

    logger.info("Application shutdown complete.")


if __name__ == "__main__":
    # 종료 신호 핸들러 등록
    signal.signal(signal.SIGINT, handle_shutdown_signal)  # Ctrl+C
    signal.signal(signal.SIGTERM, handle_shutdown_signal) # kill 명령어

    try:
        asyncio.run(main())
    except Exception as e:
         logger.critical(f"Critical error in main execution: {e}", exc_info=True)
