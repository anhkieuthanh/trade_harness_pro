import asyncio
import json
import logging
import websockets
from trade_harness.config import BINANCE_WS_URL
from trade_harness.core.portfolio import PortfolioCache

logger = logging.getLogger("trade_harness.ws")

class BinanceWSClient:
    def __init__(self, cache: PortfolioCache, ws_url: str = BINANCE_WS_URL):
        self.ws_url = ws_url
        self.cache = cache
        self.running = False

    async def start_listening(self):
        self.running = True
        logger.info(f"Connecting to Binance WebSocket: {self.ws_url}")
        while self.running:
            try:
                # Set network blind to true initially until connected
                self.cache.set_network_blind(True)
                async with websockets.connect(self.ws_url) as websocket:
                    logger.info("WebSocket connected successfully.")
                    self.cache.set_network_blind(False)
                    while self.running:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        bid = float(data.get("b", 0.0))
                        ask = float(data.get("a", 0.0))
                        timestamp = int(data.get("T", 0))
                        
                        self.cache.update_tick(bid, ask, timestamp)
            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"WebSocket connection closed: {e}. Reconnecting...")
                self.cache.set_network_blind(True)
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"WebSocket error: {e}. Reconnecting...")
                self.cache.set_network_blind(True)
                await asyncio.sleep(1)

    def stop(self):
        self.running = False
