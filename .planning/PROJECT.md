# TradeHarnessPro

## What This Is

Hệ thống giao dịch tự động (TradeHarness) tích hợp LLM chạy ngoại tuyến (offline) để phân tích trạng thái thị trường real-time và ra quyết định giao dịch trên Binance Futures cho cặp BTCUSDT. Hệ thống tách biệt luồng nhận dữ liệu tốc độ cao (asyncio Websocket) với luồng nội suy LLM có độ trễ lớn hơn.

## Core Value

Tự động hóa hoàn toàn luồng phân tích bằng LLM, tính toán khối lượng lệnh an toàn (0.5% rủi ro/lệnh) và đặt lệnh tự động trên Binance Futures với các chốt chặn rủi ro nghiêm ngặt.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Thiết lập luồng nhận dữ liệu real-time từ Binance Futures qua Websocket không bị block (Market Data Receiver)
- [ ] Xây dựng bộ Context Harness để chuẩn hóa trạng thái tài khoản, vị thế và dữ liệu thị trường làm đầu vào cho LLM
- [ ] Kết nối và gửi prompt đến LLM Gemma 2 9B chạy cục bộ qua LM Studio (localhost:1234) để nhận tín hiệu Action & Confidence
- [ ] Thiết lập Decision Harness để tính Position Size dựa trên mức rủi ro cố định 0.5% tài khoản (tùy chỉnh được) và mức Stop Loss
- [ ] Thiết lập Risk Harness kiểm tra chốt chặn an toàn: Daily drawdown < 2%, Monthly drawdown < 10%, và chặn lệnh nếu độ trễ dữ liệu timestamp > 1000ms
- [ ] Xây dựng Execute Harness thực thi đặt lệnh thực tế qua Binance Futures API
- [ ] Phát triển Supervisor ghi nhận trajectory đầy đủ (Context -> Signal -> Execution -> Outcome)
- [ ] Xây dựng bộ tải dữ liệu lịch sử Binance Futures về file CSV phục vụ Backtest

### Out of Scope

- Giao dịch nhiều cặp tiền tệ cùng lúc — Giới hạn trong cặp BTCUSDT để đảm bảo hiệu năng và độ ổn định của v1.
- Giao diện Web UI/Mobile App — Cấu hình qua file và theo dõi trực tiếp bằng log hệ thống.
- Sử dụng API LLM trả phí từ bên ngoài — Chỉ dùng Gemma 2 9B chạy offline trên LM Studio.

## Context

Hệ thống được thiết kế theo kiến trúc bất đồng bộ (asyncio) kết hợp đa tiến trình. Tiến trình Trading Engine giữ kết nối liên tục với Binance qua Websocket và cập nhật RAM Portfolio Manager, còn các yêu cầu suy luận LLM được đẩy sang LM Studio chạy cục bộ giúp loại bỏ rủi ro block thread.

## Constraints

- **Tech Stack**: Python 3.12+, `asyncio` làm core loop.
- **LLM**: Gemma 2 9B chạy offline qua LM Studio tại `http://localhost:1234/v1`.
- **Latency**: Dữ liệu timestamp cũ quá 1000ms phải bị hủy bỏ ngay lập tức ở lớp Risk Harness.
- **Risk per Trade**: Rủi ro trên mỗi trade cố định ở mức 0.5% số dư khả dụng (available balance) và có thể cấu hình được.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Sử dụng HTTP REST (OpenAI SDK / httpx) để gọi LM Studio | Đơn giản, tương thích chuẩn OpenAPI có sẵn của LM Studio, hỗ trợ async | — Pending |
| Tách biệt Engine (asyncio) và Inference (LM Studio) | Tránh nghẽn thread nhận dữ liệu tick data từ Binance Websocket | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-12 after initialization*
