# Pitfalls Research

**Domain:** Algorithmic Trading Systems (Binance Futures)
**Researched:** 2026-06-12
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Websocket Blockage due to slow LLM Inference

**What goes wrong:**
Websocket connection gets closed with `Ping timeout` or misses tick events because the thread is blocked during local LLM inference.

**Why it happens:**
Calling LM Studio models synchronous/blocking calls within the same thread that listens to websockets. Local model inference on Gemma 2 9B can take 1 to 5 seconds depending on hardware, while Binance expects heartbeat pings and continuous queue consumption.

**How to avoid:**
Use `asyncio` to make inference calls fully asynchronous (using `await` on HTTP/REST client), or separate Websocket data reception and Inference into separate processes.

**Warning signs:**
Websocket disconnects frequently; logs show `ping timeout`; latency between tick event generation on Binance and processing time in the engine grows over time.

**Phase to address:** Phase 1 (Core connection and async loop architecture).

---

### Pitfall 2: Stale Market Data Order Placement

**What goes wrong:**
The system places a market order based on LLM signals that analyzed market data from seconds ago, causing trades at bad prices.

**Why it happens:**
If the LLM inference takes 2-3 seconds, the market state has shifted. If the system does not check the age of the data when checking risk rules, it executes the stale trade.

**How to avoid:**
Implement a strict latency check in the Risk Harness. Reject/block any order if the timestamp of the context data is older than 1000ms compared to the current system time.

**Warning signs:**
Trades executing at prices far away from the entry price specified by the LLM; logs showing latency metrics above 1000ms during order prep.

**Phase to address:** Phase 2 (Decision & Risk Harness).

---

### Pitfall 3: Inadequate Drawdown Safety Controls

**What goes wrong:**
A bug in LLM generation or logic loops places repeated orders in a losing streak, blowing up the account.

**Why it happens:**
Relying solely on LLM to stop trading, without a hard-coded check of daily and monthly balance changes in the Risk Harness.

**How to avoid:**
Enforce hard-coded chốt chặn (circuit breakers) in Risk Harness: query Binance available/wallet balances before order execution, check against daily max drawdown (< 2%) and monthly max drawdown (< 10%), blocking new orders if exceeded.

**Warning signs:**
Drawdowns exceeding 2% in a single day without engine automatically pausing.

**Phase to address:** Phase 2 (Decision & Risk Harness).

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hard-coding API keys in code | Fast setup | Security leak if committed to git | Never. Use environment variables or config files |
| Skipping local database | No DB setup overhead | Lose historical trajectory logs | Acceptable only in MVP v1 where CSV files are sufficient |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Binance Futures | Placing orders without checking margin ratio | Check available balance and calculate leverage safely before placing order |
| LM Studio | Assuming 100% uptime | Implement retry mechanisms and fallbacks for local REST calls |

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Websocket disconnect | LOW | Implement auto-reconnect logic with exponential backoff |
| Stale data warning | LOW | Discard current signal, wait for next tick sequence to generate fresh context |

---
*Pitfalls research for: TradeHarnessPro*
*Researched: 2026-06-12*
