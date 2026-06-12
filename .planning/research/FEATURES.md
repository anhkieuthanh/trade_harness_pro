# Feature Research

**Domain:** Algorithmic Trading Systems (Binance Futures)
**Researched:** 2026-06-12
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Live Websocket Tick Feed | Real-time market state calculation. | MEDIUM | Python `asyncio` listener for Binance Futures `BTCUSDT@aggTrade` / `bookTicker`. |
| Context Harness | Format balances, orders, positions into clean JSON context. | LOW | Extracts from memory cache and serializes. |
| LLM Decision Generator | Asks Gemma 2 9B for BUY/SELL/HOLD and stops/targets. | MEDIUM | Async openai API client calling localhost:1234. |
| Position Sizing (Risk 0.5%) | Automatic order sizing based on stop loss distance. | LOW | Math: `qty = (balance * risk_pct) / abs(entry - stop_loss)`. |
| Risk Gate (Drawdowns/Latency)| Protects account from runaways and stale data. | MEDIUM | Stoppage if daily loss > 2%, monthly > 10%, or age > 1000ms. |
| Order Execution | Placing the order on Binance Futures exchange. | MEDIUM | Signed HMAC-SHA256 REST API calls. |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Local LLM (Gemma 2 9B) | No API costs, high privacy, infinite free inference. | MEDIUM | Requires local hardware with sufficient RAM/VRAM. |
| Trajectory Supervisor | Auditable logs of LLM reasoning vs trade outcome. | MEDIUM | Stores JSON trajectory of Context -> Signal -> Execution -> Outcome. |
| CSV Historical Downloader | Simple backtest data management. | LOW | Uses pandas and Binance Klines REST endpoint. |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Multi-pair concurrent trade | Expand profit opportunities | Increases token usage, local model concurrency issues, API limits | Focus on BTCUSDT to perfect event loop latency first |
| Cloud hosted LLM APIs | Simple setup | High API fees, latency variations, dependency on internet stability | Local LM Studio Gemma 2 9B |

## Feature Dependencies

```
[Websocket Feed] ────┐
                    ├──> [Context Harness] ──> [LLM Decision] ──> [Decision/Risk Harness] ──> [Execute Harness]
[Portfolio Manager] ─┘                                                  ▲
                                                                        │
                                                            [Supervisor Logs]
```

## MVP Definition

### Launch With (v1)

- [ ] Websocket Client — BTCUSDT Live BookTicker.
- [ ] Context Harness — Porting Account State and Binance Orderbook into prompt.
- [ ] Local Inference Agent — LM Studio + Gemma 2 9B integration.
- [ ] Decision Harness — Configurable 0.5% risk per trade calculation.
- [ ] Risk Harness — Strict daily/monthly drawdown and 1000ms latency gates.
- [ ] Execute Harness — Executing MARKET orders with SL/TP on Binance Futures.
- [ ] Supervisor — Saving full trade trajectories to local files.
- [ ] Historical Downloader & Backtest — Fetching Klines to CSV and running basic loops.

---
*Feature research for: TradeHarnessPro*
*Researched: 2026-06-12*
