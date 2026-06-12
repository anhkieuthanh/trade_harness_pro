import asyncio
import logging
from trade_harness.connection.binance_ws import BinanceWSClient

logger = logging.getLogger("trade_harness.main")

async def main():
    client = BinanceWSClient()
    try:
        await client.start_listening()
    except asyncio.CancelledError:
        logger.info("Main loop cancelled.")
    finally:
        client.stop()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Shutting down...")
