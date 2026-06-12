# Phase 2: Decision, Risk, & Execution Harness - Context

**Gathered:** 2026-06-12
**Status:** Ready for planning

<domain>
## Phase Boundary

Tính toán Position Sizing (0.5% rủi ro/lệnh), kiểm tra chốt chặn rủi ro (Drawdown, Latency) và thực thi đặt lệnh thực tế kèm cơ chế bảo hiểm SL/TP trên Binance Futures.

</domain>

<decisions>
## Implementation Decisions

### Drawdown & Redis Storage
- **D-01 (Redis Only):** Lưu baseline số dư ngày/tháng (`drawdown:daily_baseline`, `drawdown:monthly_baseline`) trực tiếp vào cơ sở dữ liệu in-memory Redis để truy xuất tốc độ cao. Không fallback sang JSON.

### Cấu hình Leverage & Margin Type
- **D-02 (Initialization Sync):** Đồng bộ cấu hình đòn bẩy `DEFAULT_LEVERAGE` và chế độ ký quỹ `MARGIN_TYPE` ( Isolated / Cross) từ `.env` lên Binance API **đúng 1 lần duy nhất** khi bot khởi động. Không gọi lại trước mỗi lệnh để tránh lỗi spam rate-limit.

### Cơ chế SL/TP
- **D-03 (Hybrid SL/TP):**
  - **Hard Protection (Khiên cứng):** Ngay khi lệnh Entry khớp, lập tức bắn 2 lệnh điều kiện `STOP_MARKET` (cắt lỗ) và `TAKE_PROFIT_MARKET` (chốt lời) treo sẵn trên sàn Binance.
  - **Soft Exit / Trailing (Khiên mềm):** Theo dõi giá trong RAM bởi khối Decision Harness để chốt lời sớm, trailing stop hoặc đảo vị thế theo tín hiệu LLM. Nếu chạm mốc mềm trước, bắn lệnh `MARKET CLOSE` đóng vị thế thủ công, đồng thời hủy (Cancel) 2 lệnh điều kiện Hard trên sàn.

### Xử lý lỗi đặt SL/TP (Naked Position)
- **D-04 (Escalation Protocol):** Nếu vị thế Entry đã khớp nhưng không thể đặt lệnh SL/TP:
  - **Bước 1 (Retry):** Thử lại tối đa 3 lần với exponential backoff cực nhỏ (200ms -> 400ms -> 800ms).
  - **Bước 2 (Panic Close):** Nếu sau 3 lần vẫn lỗi, bắn lệnh `MARKET CLOSE` ngay lập tức để đóng toàn bộ vị thế.
  - **Bước 3 (Halt & Alert):** Ghi log `CRITICAL_EXECUTION_FAILURE`, tạm dừng toàn bộ luồng Decision Harness và bắn cảnh báo Telegram (mock).

### the agent's Discretion
- Chi tiết cấu trúc dữ liệu key-value lưu trong Redis cho baseline drawdown.
- Format định dạng các payload REST API đặt lệnh Futures.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Thỏa thuận dữ liệu & API Binance Futures
- `Thiết kế Data Contracts & Database Schema.md` §3 — Cấu trúc hợp đồng đặt lệnh Futures (Order Contract).
- `Event Loop & Concurrency.md` — Mô hình tách biệt I/O và suy luận LLM.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `trade_harness/config.py`: Nạp cấu hình các giới hạn drawdown và API Keys.
- `trade_harness/core/portfolio.py`: Cache RAM chứa trạng thái giá bid/ask và tài khoản.

### Integration Points
- `trade_harness/connection/binance_rest.py`: Mở rộng thêm các hàm REST POST để đặt lệnh Market Order và Stop Market.

</code_context>

<deferred>
## Deferred Ideas

- Tích hợp chatbot/webhook Telegram/Discord thực tế để nhận tin nhắn khẩn cấp — Trích xuất thành Phase 3 hoặc v2.

</deferred>

---

*Phase: 02-decision-risk-execution-harness*
*Context gathered: 2026-06-12*
