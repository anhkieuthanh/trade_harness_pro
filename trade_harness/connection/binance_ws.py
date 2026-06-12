import asyncio
import json
import logging
import websockets
from trade_harness.config import BINANCE_WS_URL

logger = logging.getLogger("trade_harness.ws")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class BinanceWSClient:
    def __init__(self, ws_url: str = BINANCE_WS_URL):
        self.ws_url = ws_url
        self.running = False

    async def start_listening(self):
        self.running = True
        logger.info(f"Connecting to Binance WebSocket: {self.ws_url}")
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    logger.info("WebSocket connected successfully.")
                    while self.running:
                        message = await websocket.recv()
                        data = json.loads(message)
                        # Minimal log of raw tick
                        logger.info(f"Tick received: Bid {data.get('b')} / Ask {data.get('a')}")
            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"WebSocket connection closed: {e}. Reconnecting in 1s...")
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"WebSocket error: {e}. Reconnecting in 1s...")
                await asyncio.sleep(1)

    def stop(self):
        self.running = False
