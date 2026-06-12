import os
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

BINANCE_WS_URL = os.getenv("BINANCE_WS_URL", "wss://fstream.binance.com/ws/btcusdt@bookTicker")
BINANCE_REST_URL = os.getenv("BINANCE_REST_URL", "https://fapi.binance.com")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# Risk Settings
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "0.005"))
DAILY_DRAWDOWN_LIMIT = float(os.getenv("DAILY_DRAWDOWN_LIMIT", "0.02"))
MONTHLY_DRAWDOWN_LIMIT = float(os.getenv("MONTHLY_DRAWDOWN_LIMIT", "0.10"))
LATENCY_LIMIT_MS = float(os.getenv("LATENCY_LIMIT_MS", "1000.0"))
