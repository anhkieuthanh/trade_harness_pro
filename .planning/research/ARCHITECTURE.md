# Architecture Research

**Domain:** Algorithmic Trading Systems (Binance Futures)
**Researched:** 2026-06-12
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       Trading Engine                        │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌───────────────────┐  ┌────────────┐  │
│  │ Websocket Feed │  │ Portfolio Manager │  │ Supervisor │  │
│  └───────┬────────┘  └─────────┬─────────┘  └─────▲──────┘  │
│          │ Market Data         │ State            │ Logs    │
│  ┌───────▼─────────────────────▼─────────┐        │         │
│  │            Context Harness            ├────────┼──────┐  │
│  └───────────────────┬───────────────────┘        │      │  │
│                      │ Context Prompt             │      │  │
│  ┌───────────────────▼───────────────────┐        │      │  │
│  │         LM Studio (Inference)         │        │      │  │
│  └───────────────────┬───────────────────┘        │      │  │
│                      │ Signal (Action/SL/TP)      │      │  │
│  ┌───────────────────▼───────────────────┐        │      │  │
│  │           Decision & Risk Gate        ├────────┘      │  │
│  └───────────────────┬───────────────────┘               │  │
│                      │ Executable Order                  │  │
│  ┌───────────────────▼───────────────────┐               │  │
│  │              Execute Harness          │               │  │
│  └───────────────────┬───────────────────┘               │  │
└──────────────────────┼───────────────────────────────────┼──┘
                       │ Place Order                       │
                       ▼                                   ▼
               Binance Futures                    CSV Backtest Logs
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Websocket Client | Non-blocking tick data listening | `asyncio` + WebSockets / python-binance async manager |
| Portfolio Manager | Keeps available balances, open positions, order states in RAM | Local Python class updated via Websocket execution reports & user syncs |
| Context Harness | Serializes active portfolio state and ticks into Prompt | String interpolation using custom Jinja2 templates or f-strings |
| Inference Agent | Requests trading decisions from local LLM | Async HTTP client (httpx) calling LM Studio locally |
| Decision/Risk Harness | Sizing, drawdown checks, latency checks | Validation functions against memory state and local configurations |
| Execute Harness | Sends Signed Binance API requests | REST API client utilizing API Key/Secret signature generation |
| Supervisor | Stores logs of reasoning trajectories | Structured JSON logs written to local rotating file appender |

## Recommended Project Structure

```
trade_harness/
├── __init__.py
├── main.py                 # Core asyncio runner & coordinator
├── config.py               # Settings (API keys, risk params, daily limit)
├── connection/
│   ├── binance_ws.py       # Websocket data stream receiver
│   └── binance_rest.py     # Execute harness REST client
├── core/
│   ├── portfolio.py        # In-memory Portfolio Manager
│   ├── context.py          # Context Harness prompt builders
│   ├── decision.py         # Position sizing math
│   └── risk.py             # Drawdown & latency safety checks
├── inference/
│   └── lm_studio.py        # LM Studio openai-compatible client
└── utils/
    ├── supervisor.py       # Trajectory logging
    └── downloader.py       # CSV historical downloader
```

## Architectural Patterns

### Pattern 1: Async Event Loop Separated from CPU-Bound Inference
Trading Engine runs a single-threaded Python event loop (`asyncio`). Whenever it requests inference from Gemma 2 via LM Studio, it uses `await client.chat.completions.create(...)` which releases control back to the event loop. The Websocket listener continues to receive market data, appending it to the local cache, preventing buffer overflows.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Binance Futures | Async Websocket & REST HTTP API | HMAC-SHA256 signatures, API weight limits apply |
| LM Studio | HTTP REST (OpenAI SDK format) | Must run locally at `http://localhost:1234/v1` |

---
*Architecture research for: TradeHarnessPro*
*Researched: 2026-06-12*
