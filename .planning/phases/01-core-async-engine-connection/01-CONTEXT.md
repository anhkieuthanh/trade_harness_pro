# Phase 1: Core Async Engine & Connection - Context

**Gathered:** 2026-06-12
**Status:** Ready for planning

<domain>
## Phase Boundary

Thiết lập WebSocket kết nối Binance, cache Portfolio State trong RAM, kết nối async tới LM Studio.

</domain>

<decisions>
## Implementation Decisions

### WebSocket Reconnect & Circuit Breaker
- **D-01 (Exponential Backoff Tốc độ cao):** Khi rớt kết nối WebSocket từ Binance Futures, thực hiện kết nối lại với thời gian chờ tăng dần: 1s, 2s, 4s, 8s, và tối đa dừng ở 10s (không tăng thêm để tránh trễ lệnh dài nhưng không spam quá mức làm Binance chặn IP).
- **D-02 (Circuit Breaker - Cầu dao tự động):** Ngay khi mất kết nối WebSocket, phát ra cờ hiệu `NETWORK_BLIND = TRUE` toàn hệ thống.
  - Decision Harness: Đóng băng việc mở lệnh mới.
  - Risk Harness: Đặt hệ thống vào trạng thái phòng thủ, xem xét gửi lệnh REST API hủy các Limit Order đang treo rủi ro cao.
- **D-03 (REST API Fallback):** Trong thời gian WebSocket ngắt kết nối và đang thử lại, tự động chuyển sang gọi REST API `GET /fapi/v1/ticker/bookTicker` mỗi 1 giây để cập nhật cache giá thị trường tạm thời, phục vụ việc duy trì tính toán SL cứu mạng của Decision/Risk Harness.

### the agent's Discretion
- Kiến trúc chi tiết của in-memory cache cho Portfolio State.
- Cấu trúc file log và console logging format.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Thỏa thuận dữ liệu & Hướng dẫn đồng thì
- `Thiết kế Data Contracts & Database Schema.md` — Định nghĩa cấu trúc JSON của Portfolio State, Signal Contract và Order Contract.
- `Event Loop & Concurrency.md` — Phân tích bài toán Blocking thread nhận WebSocket và kiến trúc đa tiến trình/asyncio.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Không có asset tái sử dụng sẵn do đây là dự án greenfield/khởi tạo mới.

### Established Patterns
- Sử dụng mô hình `asyncio` loop làm core runner để tránh block IO.

</code_context>

<deferred>
## Deferred Ideas

- Tích hợp gửi thông báo Telegram/Discord Alerting khi Circuit Breaker được kích hoạt — Chuyển sang Phase 3 hoặc v2 (v1 tạm thời chỉ in log lỗi nghiêm trọng).

</deferred>

---

*Phase: 01-core-async-engine-connection*
*Context gathered: 2026-06-12*
