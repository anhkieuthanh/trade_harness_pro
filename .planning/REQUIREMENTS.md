# Requirements: TradeHarnessPro

**Defined:** 2026-06-12
**Core Value:** Tự động hóa hoàn toàn luồng phân tích bằng LLM, tính toán khối lượng lệnh an toàn (0.5% rủi ro/lệnh) và đặt lệnh tự động trên Binance Futures với các chốt chặn rủi ro nghiêm ngặt.

## v1 Requirements

### Core Async Engine & Connection (CONN)

- [x] **CONN-01**: Hệ thống duy trì kết nối WebSocket tới Binance Futures `bookTicker` của cặp BTCUSDT liên tục.
- [x] **CONN-02**: Hệ thống duy trì in-memory cache chứa Portfolio State (Available balance, open positions, order book) cập nhật real-time.
- [x] **CONN-03**: Hệ thống có khả năng gọi async tới LM Studio cục bộ (`http://localhost:1234/v1`) mà không làm block luồng nhận dữ liệu WebSocket.

### Context Harness (CONT)

- [x] **CONT-01**: Context Harness có khả năng đóng gói trạng thái tài khoản và orderbook thành JSON string theo đúng Schema.
- [x] **CONT-02**: Context Harness xây dựng prompt có cấu trúc rõ ràng làm đầu vào cho mô hình Gemma 2 9B.

### Decision & Risk Harness (RISK)

- [ ] **RISK-01**: Decision Harness tự động tính toán position size dựa trên mức rủi ro cấu hình được (mặc định 0.5% available balance) và khoảng cách từ entry tới Stop Loss.
- [ ] **RISK-02**: Risk Harness thực hiện chốt chặn drawdown: nếu daily drawdown vượt quá 2% hoặc monthly drawdown vượt quá 10%, hệ thống tự ngắt không đặt lệnh mới.
- [ ] **RISK-03**: Risk Harness thực hiện chốt chặn độ trễ (latency check): nếu chênh lệch timestamp giữa lúc nhận dữ liệu thị trường và thời điểm chuẩn bị gửi lệnh lớn hơn 1000ms, hủy bỏ lệnh.

### Execution Harness (EXEC)

- [ ] **EXEC-01**: Execute Harness thực thi đặt lệnh Market Order kèm theo Stop Loss và Take Profit tương ứng lên tài khoản Binance Futures thực tế thông qua các request REST API có chữ ký hợp lệ.

### Supervisor & Backtesting (SUPV)

- [ ] **SUPV-01**: Supervisor tự động lưu trữ trajectory đầy đủ (Context -> Signal -> Execution -> Outcome) dạng JSON logs cục bộ.
- [ ] **SUPV-02**: Hệ thống có bộ tải dữ liệu lịch sử Klines từ Binance Futures về file CSV.
- [ ] **SUPV-03**: Chạy backtest mô phỏng khớp lệnh offline dựa trên dữ liệu CSV đã tải.

## v2 Requirements

- **MULTI-01**: Giao dịch đa cặp tài sản đồng thời.
- **DASH-01**: Giao diện Dashboard Web theo dõi trực quan trạng thái bot.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Cloud hosted LLM APIs (OpenAI/Anthropic) | Giới hạn chi phí và bảo mật, ưu tiên chạy offline hoàn toàn qua LM Studio. |
| Multi-pair concurrent trade in v1 | Tránh quá tải event loop và bottleneck của mô hình local Gemma 2. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CONN-01 | Phase 1 | Complete |
| CONN-02 | Phase 1 | Complete |
| CONN-03 | Phase 1 | Complete |
| CONT-01 | Phase 1 | Complete |
| CONT-02 | Phase 1 | Complete |
| RISK-01 | Phase 2 | Pending |
| RISK-02 | Phase 2 | Pending |
| RISK-03 | Phase 2 | Pending |
| EXEC-01 | Phase 2 | Pending |
| SUPV-01 | Phase 3 | Pending |
| SUPV-02 | Phase 3 | Pending |
| SUPV-03 | Phase 3 | Pending |

**Coverage:**

- v1 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0 ✓

---
*Requirements defined: 2026-06-12*
*Last updated: 2026-06-12 after initial definition*
