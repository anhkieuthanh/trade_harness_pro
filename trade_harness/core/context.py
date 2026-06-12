import json
from trade_harness.core.portfolio import PortfolioCache

class ContextHarness:
    def __init__(self):
        pass

    def build_json_context(self, cache: PortfolioCache) -> dict:
        return {
            "timestamp": cache.timestamp,
            "market_data": {
                "symbol": "BTCUSDT",
                "best_bid": cache.best_bid,
                "best_ask": cache.best_ask
            },
            "portfolio": {
                "balances": cache.balances,
                "positions": cache.positions,
                "open_orders": cache.open_orders
            },
            "network_blind": cache.network_blind
        }

    def build_prompt(self, cache: PortfolioCache) -> str:
        context_data = self.build_json_context(cache)
        
        prompt = f"""
You are the Nanobot Trading Counselor for TradeHarnessPro.
Analyze the following account and market context, and return a trading decision.

CONTEXT:
{json.dumps(context_data, indent=2)}

INSTRUCTIONS:
1. You MUST respond with a valid JSON block containing:
   - "action": "LONG", "SHORT", or "HOLD"
   - "confidence": Float between 0.0 and 1.0
   - "reasoning": Brief sentence explaining the choice.
   - "sl_price": Float suggesting Stop Loss price (0.0 if HOLD)
   - "tp_price": Float suggesting Take Profit price (0.0 if HOLD)

Do NOT include any extra conversational text, code fences or markdown blocks, only the raw JSON.
"""
        return prompt.strip()
