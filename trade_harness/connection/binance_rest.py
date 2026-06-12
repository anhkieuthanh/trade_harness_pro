import logging
import httpx
from trade_harness.config import BINANCE_REST_URL

logger = logging.getLogger("trade_harness.rest")

async def fetch_book_ticker(symbol: str = "BTCUSDT") -> dict:
    url = f"{BINANCE_REST_URL}/fapi/v1/ticker/bookTicker?symbol={symbol.upper()}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                return {
                    "bid": float(data.get("bidPrice", 0.0)),
                    "ask": float(data.get("askPrice", 0.0)),
                    "timestamp": int(data.get("time", 0))
                }
            else:
                logger.error(f"Failed to fetch bookTicker from REST: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"Error fetching REST bookTicker: {e}")
    return {}
