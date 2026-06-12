# Phase 2: Decision, Risk, & Execution Harness - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-12
**Phase:** 02-decision-risk-execution-harness
**Areas discussed:** Drawdown Tracking Mechanism, Binance Futures Leverage & Margin Management, Order Execution Failures & API Error Handling

---

## Drawdown Tracking Mechanism

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Local JSON | Save daily/monthly balance baseline to drawdown_state.json | |
| 2. Dynamic Binance REST | Call Binance API dynamically to calculate baseline | |
| 3. Redis Snapshotting | Take total_wallet_balance snapshot at 00:00 UTC and save to Redis | ✓ |

**User's choice:** Sử dụng Redis làm cơ sở dữ liệu in-memory để lưu baseline drawdown, có cơ chế lưu xuống đĩa (persistence RDB/AOF) để khôi phục khi mất điện. Không fallback sang JSON.

---

## Binance Futures Leverage & Margin Management

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Synchronous check | Set leverage/margin before every order | |
| 2. Initialization Sync | Set leverage/margin mode once at startup and save state to RAM | ✓ |

**User's choice:** Chỉ thiết lập leverage và margin type isolated/cross một lần duy nhất lúc khởi động bot, lưu vào RAM. Không gọi API check lại trước mỗi lệnh để tránh lỗi rate limit.
**SL/TP:** Gửi 2 lệnh điều kiện Hard SL/TP treo sẵn trên Binance (chống sập nguồn/mất mạng), kết hợp theo dõi Soft Exit / Trailing Stop trong RAM của Decision Harness (hủy Hard orders nếu khớp Soft).

---

## Order Execution Failures & API Error Handling

| Option | Description | Selected |
|--------|-------------|----------|
| 1. Panic Close immediately | Panic close entry order on first SL/TP placement failure | |
| 2. Escalation Protocol | Retry 3 times (backoff 200ms -> 400ms -> 800ms), then Panic Close | ✓ |

**User's choice:** Thực hiện quy trình leo thang 3 bước:
1. Thử lại đặt SL/TP 3 lần.
2. Nếu vẫn lỗi, Market Close đóng vị thế Entry ngay (Panic Close).
3. Ghi log, cảnh báo Telegram, tạm dừng Decision Harness.

---

## deferred Ideas

- Thiết lập Webhook Telegram/Discord cảnh báo thực tế (Phase 3 hoặc v2).

---

*Phase: 02-decision-risk-execution-harness*
*Discussion log generated: 2026-06-12*
