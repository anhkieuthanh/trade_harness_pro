<!-- GSD:project-start source:PROJECT.md -->

## Project

**TradeHarnessPro**

Hệ thống giao dịch tự động (TradeHarness) tích hợp LLM chạy ngoại tuyến (offline) để phân tích trạng thái thị trường real-time và ra quyết định giao dịch trên Binance Futures cho cặp BTCUSDT. Hệ thống tách biệt luồng nhận dữ liệu tốc độ cao (asyncio Websocket) với luồng nội suy LLM có độ trễ lớn hơn.

**Core Value:** Tự động hóa hoàn toàn luồng phân tích bằng LLM, tính toán khối lượng lệnh an toàn (0.5% rủi ro/lệnh) và đặt lệnh tự động trên Binance Futures với các chốt chặn rủi ro nghiêm ngặt.

### Constraints

- **Tech Stack**: Python 3.12+, `asyncio` làm core loop.
- **LLM**: Gemma 2 9B chạy offline qua LM Studio tại `http://localhost:1234/v1`.
- **Latency**: Dữ liệu timestamp cũ quá 1000ms phải bị hủy bỏ ngay lập tức ở lớp Risk Harness.
- **Risk per Trade**: Rủi ro trên mỗi trade cố định ở mức 0.5% số dư khả dụng (available balance) và có thể cấu hình được.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->

## Technology Stack

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

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.agent/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
