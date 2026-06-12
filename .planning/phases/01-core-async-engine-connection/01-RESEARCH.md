# Phase 1: Core Async Engine & Connection - Research

**Phase:** 01
**Domain:** core-async-engine-connection
**Date:** 2026-06-12
**Status:** Completed

## 1. Technical Architecture & Connection

### Binance Futures bookTicker WebSocket Stream
Để lắng nghe dữ liệu giá thời gian thực mà không bị chặn, ta kết nối tới endpoint WebSocket của Binance Futures:
- URL: `wss://fstream.binance.com/ws/btcusdt@bookTicker`
- Format tin nhắn nhận được:
```json
{
  "e": "bookTicker",         // Event type
  "u": 400900217,            // order book updateId
  "s": "BTCUSDT",            // Symbol
  "b": "62500.00",           // Best bid price
  "B": "1.234",              // Best bid qty
  "a": "62500.10",           // Best ask price
  "A": "2.567",              // Best ask qty
  "T": 1718158363000         // Transaction time (millisecond)
}
```
Để duy trì kết nối này ổn định:
1. Sử dụng thư viện `websockets` (async-native) hoặc lớp client của `aiohttp` để nhận các event tuần tự.
2. Thực hiện gửi ping định kỳ (mỗi 30-50 giây) để tránh bị máy chủ Binance ngắt kết nối do Idle timeout.

### LM Studio Async Client
LM Studio chạy offline tương thích hoàn toàn với API của OpenAI. Ta sử dụng thư viện `openai` ở chế độ không đồng bộ (`AsyncOpenAI`):
- Endpoint: `http://localhost:1234/v1`
- Model: `gemma-2-9b` (hoặc mô hình đã load trên LM Studio).
- Code mẫu khởi tạo và gọi async:
```python
from openai import AsyncOpenAI

client = AsyncOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

async def get_trading_signal(prompt: str):
    response = await client.chat.completions.create(
        model="gemma-2-9b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content
```
Do sử dụng `await`, event loop của asyncio được giải phóng để tiếp tục nhận tin nhắn từ WebSocket trong khi đợi LM Studio sinh từ (inference).

## 2. In-Memory Portfolio Cache & Thread-Safety

Hệ thống chạy trên mô hình đơn luồng bất đồng bộ (Single-threaded Event Loop) của Python `asyncio`. Việc truy cập và ghi nhận dữ liệu vào `Portfolio State` trong RAM:
- Không cần các cơ chế lock khóa luồng phức tạp (như Threading locks) vì tất cả tác vụ diễn ra trên cùng một luồng.
- Cần đảm bảo các tác vụ `await` không làm thay đổi trạng thái Portfolio một cách bất hợp lệ giữa chừng (Race condition mức logic).
- Lớp cache sẽ lưu trữ cấu trúc:
```python
class PortfolioCache:
    def __init__(self):
        self.timestamp = 0
        self.balances = {}
        self.positions = []
        self.open_orders = []
        self.best_bid = 0.0
        self.best_ask = 0.0
        self.network_blind = False
```

## 3. Circuit Breaker & Fallback Design

1. **NETWORK_BLIND Flag**: Khi thư viện Websocket bắt được sự kiện ngắt kết nối (`ConnectionClosed`), ta lập tức gán `self.network_blind = True`.
2. **REST API Fallback**: Thiết lập một task chạy ngầm tuần kỳ (periodic background task) bằng `asyncio.create_task`:
   - Khi `network_blind == True`, task này sẽ bắt đầu gửi HTTP GET tới `https://fapi.binance.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT` mỗi 1 giây để cứu dữ liệu giá.
   - Khi WebSocket khôi phục và kết nối lại thành công, gán `network_blind = False` và dừng task REST fallback.

## 4. Prompt & Context Harness Construction

Prompt gửi cho Gemma 2 9B cần chứa đầy đủ Context State dạng JSON và hướng dẫn định dạng trả về để dễ phân tích (JSON output).
Cấu trúc Context JSON mẫu:
```json
{
  "timestamp": 1718158363000,
  "market_data": {
    "symbol": "BTCUSDT",
    "best_bid": 62500.00,
    "best_ask": 62500.10
  },
  "portfolio": {
    "balance": 9300.00,
    "position": {
      "side": "LONG",
      "entry_price": 62500.00,
      "unrealized_pnl": 120.00
    }
  }
}
```

---
*Research completed: 2026-06-12*
*Ready for planning: yes*
