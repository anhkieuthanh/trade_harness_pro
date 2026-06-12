# Roadmap: TradeHarnessPro

## Overview

TradeHarnessPro sẽ được xây dựng theo mô hình Vertical MVP. Chúng ta đi từ thiết lập kết nối không bị nghẽn (Phase 1), sang xây dựng các quy tắc ra quyết định, chốt chặn rủi ro và thực thi đặt lệnh thực tế (Phase 2), và cuối cùng là hoàn thiện các tính năng ghi logs giám sát hành trình (Supervisor) cùng bộ tải dữ liệu CSV và Backtest (Phase 3).

## Phases

- [x] **Phase 1: Core Async Engine & Connection** - Thiết lập WebSocket kết nối Binance, cache Portfolio State trong RAM, kết nối async tới LM Studio. (completed 2026-06-12)
- [ ] **Phase 2: Decision, Risk, & Execution Harness** - Tính Position Sizing (0.5% risk), kiểm tra chốt chặn drawdown và latency, đặt lệnh Binance API.
- [ ] **Phase 3: Supervisor Logging & Backtesting** - Ghi logs trajectory đầy đủ, tải dữ liệu lịch sử CSV và chạy Backtest mô phỏng.

## Phase Details

### Phase 1: Core Async Engine & Connection

**Goal**: Thiết lập WebSocket kết nối Binance, cache Portfolio State trong RAM, kết nối async tới LM Studio.
**Mode**: mvp
**Depends on**: Nothing (first phase)
**Requirements**: CONN-01, CONN-02, CONN-03, CONT-01, CONT-02
**Success Criteria** (what must be TRUE):

  1. Engine duy trì kết nối WebSocket tới Binance Futures bookTicker BTCUSDT và in log giá liên tục mà không bị nghẽn loop.
  2. Portfolio State lưu trữ đầy đủ trong RAM (Available balance, positions, open orders) và cập nhật tức thời theo tin nhận từ WS.
  3. Engine có thể thực hiện gọi bất đồng bộ (async API call) đến LM Studio Gemma 2 9B cục bộ và nhận phản hồi thành công.

**Plans**: 3 plans

Plans:

- [x] 01-01: Khởi tạo cấu trúc source code, cấu hình môi trường và kết nối WebSocket Binance
- [x] 01-02: Xây dựng cấu trúc in-memory Portfolio State cache và bộ lọc dữ liệu
- [x] 01-03: Hiện thực hóa client kết nối async tới LM Studio và template Prompt Context Harness

### Phase 2: Decision, Risk, & Execution Harness

**Goal**: Tính Position Sizing (0.5% risk), kiểm tra chốt chặn drawdown và latency, đặt lệnh Binance API.
**Mode**: mvp
**Depends on**: Phase 1
**Requirements**: RISK-01, RISK-02, RISK-03, EXEC-01
**Success Criteria** (what must be TRUE):

  1. Position sizing được tính toán tự động dựa trên mức rủi ro cấu hình (mặc định 0.5% account available balance) và khoảng cách Stop Loss.
  2. Hệ thống dừng đặt lệnh mới ngay lập tức nếu Daily Drawdown > 2% hoặc Monthly Drawdown > 10%.
  3. Hệ thống chặn đặt lệnh nếu độ trễ dữ liệu timestamp từ Binance WebSocket đến thời điểm ra quyết định > 1000ms.
  4. Lệnh Market kèm SL/TP được gửi thành công lên tài khoản Binance Futures thật (hoặc Testnet).

**Plans**: 3 plans

Plans:

- [ ] 02-01: Thiết lập Decision Harness tính Position Sizing động
- [ ] 02-02: Hiện thực hóa Risk Harness kiểm tra chốt chặn drawdown và latency
- [ ] 02-03: Tích hợp REST API ký đặt lệnh Market Order kèm TP/SL lên Binance Futures

### Phase 3: Supervisor Logging & Backtesting

**Goal**: Ghi logs trajectory đầy đủ, tải dữ liệu lịch sử CSV và chạy Backtest mô phỏng.
**Mode**: mvp
**Depends on**: Phase 2
**Requirements**: SUPV-01, SUPV-02, SUPV-03
**Success Criteria** (what must be TRUE):

  1. Supervisor lưu lại đầy đủ JSON trajectory logs của từng nhịp ra quyết định giao dịch.
  2. Hệ thống tải thành công dữ liệu lịch sử Klines từ Binance lưu vào file CSV cục bộ.
  3. Backtester chạy hoàn chỉnh một chu kỳ mô phỏng lệnh dựa trên dữ liệu CSV đã tải và xuất báo cáo kết quả.

**Plans**: 2 plans

Plans:

- [ ] 03-01: Phát triển Supervisor ghi nhận trajectory logs
- [ ] 03-02: Phát triển module tải dữ liệu lịch sử CSV và công cụ Backtest offline

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Async Engine & Connection | 3/3 | Complete    | 2026-06-12 |
| 2. Decision, Risk, & Execution Harness | 0/3 | Not started | - |
| 3. Supervisor Logging & Backtesting | 0/2 | Not started | - |
