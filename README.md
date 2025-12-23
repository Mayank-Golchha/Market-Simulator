# 📈 Market Simulator

A Python-based market simulator that models basic exchange mechanics using a limit order book, multiple trader types, and price–time priority matching.

This project focuses on understanding how **price formation, liquidity, and supply–demand imbalance** emerge from interactions between different market participants. It is built for **learning and experimentation**, not profitability.

---

## 🎯 Objectives

- Understand **price discovery** in a limit order book  
- Study **liquidity, spread, and depth dynamics**  
- Observe effects of **order flow imbalance**
- Experiment with different **trader behaviors and strategies**

---

## ⚙️ Core Features

- Limit Order Book with **price–time priority**
- Level 2 market depth (bid/ask ladders)
- Candlestick (OHLCV) generation
- Multiple interacting trader archetypes
- Configurable parameters for experimentation
- Visual simulation using **PyQt**

---

## 🧑‍💼 Trader Types Implemented

### 🔹 Random Traders
- Place buy or sell orders randomly
- Random order size and price selection
- Provide background noise similar to retail flow

---

### 🔹 Level 1 Traders (Momentum-Based)
- Observe the **last _N_ candles**
- Trade if price change exceeds a threshold (e.g. ±1%)
- Simple momentum-following behavior

---

### 🔹 Level 2 Traders (Indicator-Based)
- Use technical indicators such as:
  - EMA
  - RSI
  - VWAP
  - Bollinger Bands
- Decisions based on indicator signals and order book imbalance
- Represent more informed or systematic traders

---

### 🔹 Level 3 Traders (Strategy-Driven)
- Combine multiple signals and strategies
- Adaptive behavior based on:
  - Market conditions
  - Liquidity
  - Volatility
- Can switch between aggressive and passive execution

---

### 🔹 Market Makers
- Place **limit buy and sell orders simultaneously**
- Earn spread by providing liquidity
- Adjust quotes based on:
  - Inventory
  - Spread
  - Order book pressure
- Key contributors to price convergence and stability

---

### 🔹 Company / Institutional Trader
- Represents a firm buying its own stock or a long-term investor
- Trades **rarely**, but in **large quantities**
- Minimal reaction to short-term price movements
- Can significantly move the market when active

---

