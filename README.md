# 🚀 TradeNova CLI

A simple and structured Python-based trading bot that places **MARKET** and **LIMIT** orders on the Binance Futures Testnet (USDT-M).
Built with clean architecture, logging, validation, and CLI support.

---

## 📌 Features

* ✅ Place **MARKET** and **LIMIT** orders
* ✅ Supports both **BUY** and **SELL**
* ✅ CLI-based input using argparse
* ✅ Input validation (symbol, quantity, price, etc.)
* ✅ Structured code (client, orders, validators)
* ✅ Logging of:

  * API requests
  * API responses
  * Errors
* ✅ Exception handling (API errors, invalid inputs, network issues)

---

## 🏗️ Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   ├── logging_config.py  # Logging setup
│
├── cli.py                 # CLI entry point
├── requirements.txt
├── README.md
├── logs/
│   └── trading.log
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/trading-bot.git
cd trading-bot
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create Binance Testnet Account

1. Go to Binance Futures Testnet
   👉 [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

2. Log in with your Binance account

3. Generate API keys

   * API Key
   * Secret Key

---

### 5️⃣ Configure API Keys

Create a `.env` file in the root directory:

```
API_KEY=your_api_key_here
API_SECRET=your_secret_key_here
BASE_URL=https://testnet.binancefuture.com
```

---

## ▶️ How to Run

### 📌 MARKET Order Example

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

### 📌 LIMIT Order Example

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

---

## 🧾 Sample Output

```
🚀 Placing Order...

Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.001

✅ Order Successful!
Order ID: 12345678
Status: FILLED
Executed Qty: 0.001
Avg Price: 64000.00
```

---

## 🪵 Logging

Logs are stored in:

```
logs/trading_bot_20260423_081111.log
```

Includes:

* Request payloads
* API responses
* Errors and exceptions

---

## ⚠️ Error Handling

The application handles:

* ❌ Invalid inputs (negative quantity, missing price)
* ❌ API errors (invalid symbol, insufficient balance)
* ❌ Network failures
* ❌ Timestamp sync issues

---

## 📦 Requirements

Example `requirements.txt`:

```
python-binance
python-dotenv
requests
```

---

## 🧠 Assumptions

* User has a valid Binance Futures Testnet account
* API keys are correctly configured
* Testnet has sufficient USDT balance
* Internet connection is stable

---

## ⭐ Bonus (Optional Feature Implemented)

✔ Improved CLI validation messages for better user experience

---

## 🧪 Test Logs Included

The repository includes logs for:

* ✅ One MARKET order
* ✅ One LIMIT order

---

## 📬 Future Improvements

* Add Stop-Limit / OCO orders
* Add UI dashboard
* Add strategy-based trading (Grid / TWAP)
* Docker support

---

## 📄 License

This project is for evaluation/demo purposes.

