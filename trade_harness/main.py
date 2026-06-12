import asyncio
import logging
from trade_harness.core.portfolio import PortfolioCache
from trade_harness.connection.binance_ws import BinanceWSClient
from trade_harness.connection.binance_rest import fetch_book_ticker

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("trade_harness.main")

async def rest_fallback_loop(cache: PortfolioCache):
    logger.info("REST fallback loop started.")
    while True:
        try:
            if cache.network_blind:
                ticker = await fetch_book_ticker("BTCUSDT")
                if ticker:
                    cache.update_tick(ticker["bid"], ticker["ask"], ticker["timestamp"])
                    logger.warning(f"[FALLBACK] Price updated via REST: Bid {ticker['bid']} / Ask {ticker['ask']}")
            await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in REST fallback loop: {e}")
            await asyncio.sleep(1.0)

async def main():
    cache = PortfolioCache()
    client = BinanceWSClient(cache)
    
    # Run REST fallback task in the background
    fallback_task = asyncio.create_task(rest_fallback_loop(cache))
    
    try:
        await client.start_listening()
    except asyncio.CancelledError:
        logger.info("Main loop cancelled.")
    finally:
        client.stop()
        fallback_task.cancel()
        await asyncio.gather(fallback_task, return_exceptions=True)
        logger.info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Shutting down...")
