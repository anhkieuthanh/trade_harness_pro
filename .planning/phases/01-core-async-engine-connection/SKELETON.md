# Walking Skeleton — TradeHarnessPro

**Phase:** 1
**Generated:** 2026-06-12

## Capability Proven End-to-End

Bot khởi chạy loop asyncio, duy trì kết nối WebSocket Binance Futures BTCUSDT bookTicker, cache giá best bid/ask, gửi Context thô sang LM Studio (Gemma 2 9B) và nhận về tín hiệu giao dịch thô hiển thị trên log.

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Runtime | Python 3.12 + asyncio | Tiêu chuẩn phát triển bot trading, hỗ trợ I/O không đồng bộ hiệu năng cao. |
| Data Layer | In-memory RAM Cache + Local CSV | Tối ưu hóa độ trễ ghi dữ liệu tick data và đơn giản hóa lưu trữ MVP. |
| Inference API | Local LM Studio HTTP API | Chạy Gemma 2 9B offline, tiết kiệm chi phí và bảo mật dữ liệu. |
| Directory Layout | Modular package under `trade_harness/` | Tách biệt các module I/O (WebSocket/REST), Core (Cache/Risk), và Utilities. |

## Stack Touched in Phase 1

- [x] Project scaffold (Python package structure, `.env` config, linter & test runner setup)
- [x] Async connection — WebSocket Binance bookTicker receiver loop
- [x] Cache management — in-memory cache holding bid/ask and available balance
- [x] LLM integration — async client sending prompt and parsing signal from local LM Studio
- [x] Execution target — local execution loop running continuously in dev mode

## Out of Scope (Deferred to Later Slices)

- Đặt lệnh thực tế lên sàn Binance Futures (Harness đặt lệnh thực tế) — Deferred to Phase 2.
- Tính Position Sizing dựa trên 0.5% risk — Deferred to Phase 2.
- Kiểm tra Drawdown và Latency safety checks — Deferred to Phase 2.
- Module Backtest và downloader dữ liệu lịch sử CSV — Deferred to Phase 3.

## Subsequent Slice Plan

- Phase 2: Quyết định position sizing, kiểm tra drawdown/latency risk chốt chặn và đặt lệnh thực tế Binance Futures API.
- Phase 3: Trajectory logs chi tiết qua Supervisor, bộ tải dữ liệu CSV và động cơ Backtest offline.
