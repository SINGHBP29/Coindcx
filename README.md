# Coindcx

![image](https://github.com/user-attachments/assets/096108cb-9281-4ed3-b63d-f0852918eeb2)
![image](https://github.com/user-attachments/assets/b0afe651-e5bd-498d-805f-e30d376fbca6)



# 🪙 CoinDCX Trading Platform

Sure! Here's a **Project Explanation** section you can directly add to your `README.md` (or use separately in your proposal/portfolio):

---

## 🧩 Project Explanation

### 🎯 Objective

The **CoinDCX Trading Platform** aims to create an intelligent and user-friendly crypto trading assistant using the CoinDCX exchange API. It enables users to interact with live market data, manage their crypto portfolio, place/cancel orders, and receive strategic insights — all through a seamless **Streamlit** web interface and a **modular backend** powered by **CrewAI agents (non-LLM)**.

---

### 🛠️ Approach

The platform is designed with a **microservice-style architecture**, consisting of separate components for API interaction, user portfolio management, order handling, and agent-based market analysis. The app is responsive, modular, and deployable both **locally** and **on Streamlit Cloud**.

---

### 🌟 Key Features Implemented

| Feature | Description |
|--------|-------------|
| **Authentication** | Simple user login/registration via unique `user_id`, stored in Redis. |
| **Live Market Viewer** | Fetches and filters INR-paired crypto data with last price, volume, 24h change. |
| **Portfolio Tracker** | Displays live holdings, locked funds, and estimated INR value using CoinDCX balances + market prices. |
| **Buy/Sell Orders** | Place market or limit buy/sell orders through the secure API interface. |
| **Order Management** | View current active orders, cancel specific ones, and check trade history. |
| **Agent-Based Analysis** | Two rule-based agents simulate human-like logic to detect market trends and advise trades. |
| **FAISS Search Engine** | Users can add and search custom strategy/data text using semantic vector retrieval. |
| **Redis Caching** | Speeds up repeat data access (e.g., balances, orders) and simulates session-based memory. |

---

### 🧠 How the Platform Works

1. **User logs in or registers** with a simple `user_id` (no passwords required). The ID is tracked in **Redis** for data caching.
2. On login, users can:
   - View **filtered live market data** from CoinDCX.
   - See a **snapshot of their portfolio** using account balance + market price.
   - Place **buy/sell orders** (limit or market type).
   - Check and manage **active orders** or **historical trades**.
3. In the **"Agent Analysis"** tab:
   - A **Market Analyst Agent** calculates average vs. current price and labels trends as bullish/bearish.
   - A **Trade Advisor Agent** provides trade suggestions based on market outlook and portfolio data.
   - No LLM is used — logic is 100% interpretable and rule-based.
4. In the **FAISS section**, users can:
   - Input and vectorize strategy notes or logs.
   - Perform **semantic search** for related entries.
   - All embeddings are stored locally using `sentence-transformers`.

---

Let me know if you'd like this turned into a portfolio PDF, presentation slide, or GitHub `README` version with visuals!

---

## 🚀 Features

  - 👤 **User Authentication & Caching** – Login/Register using a simple `user_id`, stored with Redis.
  - 📈 **Live Market Data** – Search and view current INR-based markets with price/volume metrics.
  - 💼 **Portfolio Viewer** – View current holdings, locked balances, and INR value estimations.
  - 💸 **Trade Execution** – Place market/limit buy/sell orders securely.
  - 📃 **Order Management** – View, cancel, and track current or historical orders.
  - 🤖 **Agent Analysis** – Get trading suggestions from rule-based CrewAI agents (no LLM required).
  - 🔍 **FAISS Integration** – Semantic vector search for embedded historical text data (e.g., logs, strategies).
  - 🔐 **Secure API Handling** – CoinDCX API credentials handled with `.env` and HMAC SHA256 signing.
  
``
## 📂 Project Structure

 ![image](https://github.com/user-attachments/assets/842c2692-c17d-453e-8904-4fb9f8b8798e)


 ```` 
 ## 📦 Installation
  
  ### 1. Clone the Repository
  
  ```bash
  git clone [https://github.com/yourusername/coindcx-trading-platform.git](https://github.com/SINGHBP29/Coindcx/edit/main/)
  cd coindcx-trading-platform
```

### 2. Setup Python Environment

```bash
pip install -r requirements.txt
```

### 3. Add API Credentials

Create a `.env` file in the root directory:

```env
COINDCX_API_KEY=your_api_key
COINDCX_API_SECRET=your_api_secret
```

These are used securely for authenticated API calls.

---

## ▶️ Running the App

### Streamlit UI (Recommended)

```bash
streamlit run app.py
```

### Terminal CLI (Optional)

```bash
python main.py
```

---

## 🔍 AI Agent Analysis (No LLMs Required)

Simulated agents use historical market data to analyze trends and provide suggestions:

- **Market Analyst Agent**: Identifies bullish/bearish patterns using price averages.
- **Trade Advisor Agent**: Recommends actions based on portfolio and market conditions.

No cloud inference or LLMs are needed — logic is purely rule-based and local.

---

## ⚡ Redis & FAISS Integration

- **Redis**: Caches user data (e.g., portfolio, active orders) for fast reloads.
- **FAISS**: Allows semantic search of trading logs, market summaries, or any vectorized text data.

---

```toml
COINDCX_API_KEY = "your_key"
COINDCX_API_SECRET = "your_secret"
```

5. Deploy and share the public link 🎉

---

## ✅ TODO / Enhancements

- [ ] Add chart-based portfolio visualization
- [ ] Webhooks / Telegram alerts for trade events
- [ ] User-level analytics with FAISS insights
- [ ] Role-based access & multi-user dashboards

---

## 🧠 Credits

Made with ❤️ using:

- [CoinDCX API]
- [Streamlit]
- [FAISS by Meta]
- [Redis]
- [AI Agents]

---

## 📜 License

MIT License. Use it, fork it, improve it!

---

## 🙌 Author

**Your Name**  
📫 Connect: [LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/yourusername)

