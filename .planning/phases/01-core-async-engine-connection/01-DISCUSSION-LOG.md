# Phase 1: Core Async Engine & Connection - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-12
**Phase:** 01-core-async-engine-connection
**Areas discussed:** WebSocket Reconnect & Heartbeat

---

## WebSocket Reconnect & Heartbeat

| Option | Description | Selected |
|--------|-------------|----------|
| 1. High-speed Exponential Backoff | Exponential backoff capped at 10 seconds: 1s, 2s, 4s, 8s, 10s. | ✓ |
| 2. Limited retries | Try reconnecting N times, then crash bot. | |

**User's choice:** Circuit Breaker & Fallback với Exponential Backoff tốc độ cao, kích hoạt NETWORK_BLIND = TRUE, kích hoạt REST API Fallback `GET /fapi/v1/ticker/bookTicker` mỗi 1s khi mất mạng để cứu SL, và phát cảnh báo Telegram/Discord.
**Notes:** 
- Thiết lập ngay cờ NETWORK_BLIND = TRUE để đóng băng Decision Harness (không mở vị thế mới) và đặt Risk Harness vào chế độ phòng thủ (xem xét hủy Limit Order).
- Khi mất kết nối WS, thăm dò giá qua REST API mỗi 1 giây làm giải pháp dự phòng tạm thời.

---

## the agent's Discretion

- Quyết định cấu trúc lưu trữ cache của Portfolio State trong memory.
- Lựa chọn thư viện cụ thể để kết nối WebSockets (ví dụ: native websockets vs python-binance).

## Deferred Ideas

- Gửi tin nhắn cảnh báo khẩn cấp qua Telegram/Discord webhook khi mất kết nối WebSocket (chuyển sang Phase 3 hoặc v2).

---

*Phase: 01-core-async-engine-connection*
*Discussion log generated: 2026-06-12*
