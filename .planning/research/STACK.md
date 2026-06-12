# Stack Research

**Domain:** Algorithmic Trading Systems (Binance Futures)
**Researched:** 2026-06-12
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.12+ | Core system development | Standard for algo trading, rich library ecosystem, robust support for concurrency (`asyncio`) and data analysis. |
| asyncio | Standard | Concurrency engine | Allows handling real-time high-throughput Websocket feeds (Binance) without blocking CPU resources. |
| LM Studio | 0.2.x+ | Local LLM Serving | Exposes a local OpenAI-compatible API to run Gemma 2 9B offline on consumer hardware (e.g., Mac M-series/RTX GPUs). |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| openai | 1.x.x | OpenAI-compatible API client | Used to call LM Studio's local endpoint asynchronously. |
| aiohttp / httpx | Latest | Asynchronous HTTP client | Communicating with Binance REST API and fallback endpoints. |
| pandas | Latest | Data loading, CSV manipulation | Essential for downloading historical Klines and preparing Backtest data. |
| python-binance | Latest | Binance API Wrapper | Built-in async websocket and API support for Binance. |
| pydantic | 2.x | Data validation & contracts | Ensures Portfolio State, Signal Contracts, and Order Contracts match database schema exactly. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| LM Studio | Local Gemma 2 9B model server | Needs to run on `http://localhost:1234` with OpenAI API compatibility active. |

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| LM Studio | Ollama | If deploying in headless Linux environments; Ollama's API is also OpenAI-compatible. |
| python-binance | Native websockets | If python-binance introduces overhead or lacks specific Binance Futures features. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| synchronous requests | Block the entire event loop, causing Websocket timeouts and delayed trades | `aiohttp`, `httpx` or async SDK wrappers |
| Multi-threading | Python GIL prevents parallel CPU execution; complex thread safety issues | `asyncio` for I/O and subprocesses for heavy LLM serving |

## Sources

- [Binance Futures API Docs] — verified official rate limits and endpoint structures.
- [LM Studio API reference] — verified OpenAI compatibilities.

---
*Stack research for: TradeHarnessPro*
*Researched: 2026-06-12*
