# Project Research Summary

**Project:** TradeHarnessPro
**Domain:** Algorithmic Trading Systems (Binance Futures + Local LLM)
**Researched:** 2026-06-12
**Confidence:** HIGH

## Executive Summary

TradeHarnessPro is a real-time algorithmic trading system for Binance Futures BTCUSDT. It integrates a local Gemma 2 9B model (hosted via LM Studio) as its reasoning agent to analyze market context and output trading decisions. Due to the high frequency of Binance tick data and the multi-second latency of local LLM inference, the system's core architecture must separate the I/O-bound WebSocket listener from the CPU/GPU-bound model inference to prevent thread blocking and network disconnects.

A secure risk-management harness will be implemented to automatically size positions based on a configurable 0.5% risk per trade, enforce daily/monthly drawdown boundaries, and block orders when latency spikes above 1000ms.

## Key Findings

### Recommended Stack

**Core technologies:**
- **Python 3.12 (with asyncio)**: For async event loop and concurrency.
- **LM Studio (Gemma 2 9B)**: Serving local LLM offline on localhost:1234 using an OpenAI-compatible API.
- **python-binance**: For async WebSocket streams and signed REST orders.

### Expected Features

**Must have (table stakes):**
- Websocket Tick Feed (bookTicker/aggTrade).
- Context Harness (prompt assembly from state/orderbook).
- Offline Inference Client (OpenAI SDK).
- Position Sizing (0.5% risk per trade based on SL).
- Risk Gate (Drawdown < 2% daily, < 10% monthly, Latency < 1000ms).
- Execute Harness (MARKET orders with TP/SL).

**Should have (competitive):**
- Trajectory Supervisor (logs Context -> Signal -> Execution -> Outcome).
- CSV Downloader (downloading historical Klines for backtest).

### Architecture Approach

**Major components:**
1. **Trading Engine (asyncio loop)**: Handles WebSocket, maintains Portfolio State.
2. **Context Harness**: Prepares dynamic prompts.
3. **Inference Client**: Communicates asynchronously with LM Studio.
4. **Decision & Risk Harness**: Math validation, drawdown gates, stale data blocking.
5. **Execute Harness**: Sends authenticated orders to Binance Futures.
6. **Supervisor**: Local file logger for trajectory audits.

### Critical Pitfalls

1. **Websocket Blockage** — Avoided by using async-native client calls (`await`) which releases the loop.
2. **Stale Market Data Trades** — Avoided by checking that context timestamps are < 1000ms old.
3. **Account Blowout** — Avoided by hard-coded daily (< 2%) and monthly (< 10%) drawdown circuit breakers.

## Implications for Roadmap

### Phase 1: Core Async Engine & Data Streams
- **Rationale**: Establish connection stability and asynchronous separation first.
- **Delivers**: WebSocket tick feed, Portfolio State caching in RAM, and basic async client for LM Studio.
- **Addresses**: Tick feeding, basic context caching.
- **Avoids**: Thread blocking (Pitfall 1).

### Phase 2: Decision, Risk, & Execution Harness
- **Rationale**: Implement trading logic, risk boundaries, and execution functions.
- **Delivers**: 0.5% risk position sizing, daily/monthly drawdown limits, 1000ms latency filter, and Binance order execution.
- **Addresses**: Risk gates, position sizing, order execution.
- **Avoids**: Stale data (Pitfall 2), account drawdown runaway (Pitfall 3).

### Phase 3: Supervisor Logging, CSV Downloader, & Backtest
- **Rationale**: Enhance observability and support offline evaluation.
- **Delivers**: Trajectory log capture, historical CSV data downloads, and backtesting loop.
- **Addresses**: Supervisor, CSV download, backtest.

---
*Research completed: 2026-06-12*
*Ready for roadmap: yes*
