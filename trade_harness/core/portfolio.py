import time
import logging

logger = logging.getLogger("trade_harness.portfolio")

class PortfolioCache:
    def __init__(self):
        self.timestamp = int(time.time() * 1000)
        self.balances = {
            "USDT": {
                "total_wallet_balance": 0.0,
                "locked_margin": 0.0,
                "available_balance": 0.0
            }
        }
        self.positions = []
        self.open_orders = []
        self.best_bid = 0.0
        self.best_ask = 0.0
        self.network_blind = False

    def update_tick(self, bid: float, ask: float, timestamp: int = None):
        self.best_bid = bid
        self.best_ask = ask
        self.timestamp = timestamp or int(time.time() * 1000)
        logger.debug(f"Cache tick updated: Bid {self.best_bid} / Ask {self.best_ask}")

    def update_balance(self, asset: str, total_wallet: float, locked: float, available: float):
        self.balances[asset] = {
            "total_wallet_balance": total_wallet,
            "locked_margin": locked,
            "available_balance": available
        }
        self.timestamp = int(time.time() * 1000)
        logger.info(f"Balance updated for {asset}: Available {available}")

    def set_network_blind(self, status: bool):
        self.network_blind = status
        logger.warning(f"NETWORK_BLIND flag set to {status}")
