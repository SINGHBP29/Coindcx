# Coindcx

![image](https://github.com/user-attachments/assets/096108cb-9281-4ed3-b63d-f0852918eeb2)
![image](https://github.com/user-attachments/assets/b0afe651-e5bd-498d-805f-e30d376fbca6)


```markdown
# 🪙 CoinDCX Trading Platform

A full-featured crypto trading dashboard built with **Streamlit**, powered by **Redis**, **FAISS**, and **CrewAI Agents (non-LLM)**. The platform integrates directly with the **CoinDCX API** and provides a rich user experience for managing your crypto assets, analyzing the market, and simulating smart agent-based decisions.

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

---

## 📂 Project Structure

![image](https://github.com/user-attachments/assets/842c2692-c17d-453e-8904-4fb9f8b8798e)

---

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

