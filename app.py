import json
import streamlit as st
from main import TradingApp, load_credentials
import faiss
import os
from sentence_transformers import SentenceTransformer
import uuid
from redis_cache import cache_data, get_cached_data, redis_client
import sys
import torch
import pandas as pd
from api_service import CoinDCXApiService  # Importing the CoinDCX API service
from ai_agents import SimulatedTradingAgent  # Importing the LLM-based analysis function

# Remove torch from module watcher
sys.modules['torch'].__path__ = []

# Load credentials
api_key, api_secret = load_credentials()

# Initialize CoinDCX API client
coindcx = CoinDCXApiService(api_key, api_secret)

# Initialize Trading App
app = TradingApp(api_key, api_secret)

# Streamlit page config
st.set_page_config(page_title="CoinDCX Trading Platform", layout="centered")
st.title("🪙 CoinDCX Trading Platform")

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

# --- User ID Section ---
if not st.session_state["is_logged_in"]:
    st.subheader("👤 User Login / Registration")
    user_id = st.text_input("🔑 Enter your User ID")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            if user_id == "":
                st.warning("Please enter a user ID.")
            elif redis_client.exists(user_id):
                st.session_state["user_id"] = user_id
                st.session_state["is_logged_in"] = True
                st.success(f"✅ Successfully logged in as {user_id}")
                st.rerun()
            else:
                st.error("❌ User ID does not exist. Please register first.")

    with col2:
        if st.button("📝 Register"):
            if user_id == "":
                st.warning("Please enter a user ID.")
            elif redis_client.exists(user_id):
                st.error("🚫 User ID already exists. Try a different one.")
            else:
                # Create user directory and initialize data
                user_dir = f"user_data/{user_id}"
                os.makedirs(user_dir, exist_ok=True)

                # Initialize empty user data
                user_data = {
                    "portfolio": [],
                    "orders": [],
                    "trades": [],
                    "deposits": []
                }

                with open(f"{user_dir}/user.json", "w") as f:
                    json.dump(user_data, f, indent=4)

                # Store user ID in Redis
                redis_client.set(user_id, "registered")
                st.session_state["user_id"] = user_id
                st.session_state["is_logged_in"] = True
                
                st.success(f"✅ User {user_id} registered successfully!")
                st.rerun()
else:
    # Show logged-in user info and logout button
    st.sidebar.success(f"Logged in as: {st.session_state['user_id']}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state["user_id"] = None
        st.session_state["is_logged_in"] = False
        st.rerun()

    # Sidebar menu (only show when logged in)
    menu = st.sidebar.radio(
        "Navigation",
        [
            "Market Data",
            "View Portfolio",
            "Place Buy Order",
            "Place Sell Order",
            "View Active Orders",
            "Cancel Order",
            "View Order History",
            "Agent Analysis"
        ]
    )

    # 1. Market Data
    if menu == "Market Data":
        st.subheader("📈 Live Market Data")
        filter_market = st.text_input("Filter by symbol (e.g., BTC, ETH):", "")
        if st.button("View Market"):
            try:
                df = app.market_service.get_ticker_dataframe(filter_market)
                if df.empty:
                    st.warning("No market data available.")
                else:
                    st.markdown("### 🔍 Filtered Market Overview")

                    # Convert numeric columns
                    numeric_cols = ["Last Price", "High", "Low", "Volume"]
                    for col in numeric_cols:
                        df[col] = pd.to_numeric(df[col], errors='coerce')  # handle any bad data

                    st.dataframe(
                        df.style.format({
                            "Last Price": "{:.6f}",
                            "High": "{:.6f}",
                            "Low": "{:.6f}",
                            "Volume": "{:.4f}",
                            "Change %": "{}"
                        }),
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error loading market data: {e}")

    # 2. View Portfolio
    elif menu == "View Portfolio":
        st.subheader("💼 Your Portfolio")

        if st.button("Refresh Portfolio"):
            try:
                # Fetch portfolio data from the account service
                portfolio = app.account_service.get_account_balance()

                # Cache the portfolio data with both user_id and key ("portfolio")
                cache_data(st.session_state["user_id"], "portfolio", portfolio)

                # Retrieve the portfolio data from cache
                # Pass both user_id and key ("portfolio") here
                cached_portfolio = get_cached_data(st.session_state["user_id"], "portfolio")

                # Display portfolio if it exists in cache
                if cached_portfolio:
                    # Convert to DataFrame for better display
                    portfolio_df = pd.DataFrame(cached_portfolio)
                    st.dataframe(portfolio_df, use_container_width=True)
                else:
                    st.info("No portfolio data available.")
            except Exception as e:
                st.error(f"Error fetching portfolio: {e}")

    # 3. Place Buy Order
    elif menu == "Place Buy Order":
        st.subheader("💵 Place Buy Order")

        market = st.text_input("Market (e.g., BTCUSDT)", "BTCUSDT")
        order_type = st.selectbox("Order Type", ["Market Order", "Limit Order"])
        quantity = st.number_input("Quantity to Buy", min_value=0.0001, step=0.0001)
        price = None

        if order_type == "Limit Order":
            price = st.number_input("Limit Price", min_value=0.01, step=0.01)

        place_order_button = st.button("Place Buy Order")
        
        if place_order_button:
            try:
                if order_type == "Market Order":
                    response = app.order_service.place_market_order(
                        market=market,
                        side="buy",
                        quantity=quantity,
                        user_id=st.session_state["user_id"]
                    )
                    st.success(f"✅ Market Buy Order placed! Quantity: {quantity},Price: {price}, Response: {response}")
                elif order_type == "Limit Order" and price:
                    response = app.order_service.place_limit_order(
                        market=market,
                        side="buy",
                        quantity=quantity,
                        price=price,
                        user_id=st.session_state["user_id"]
                    )
                    st.success(f"✅ Limit Buy Order placed! Quantity: {quantity}, Price: {price}, Response: {response}")
                else:
                    st.error("❌ Limit price is required for limit orders.")
            except Exception as e:
                st.error(f"Error placing buy order: {e}")


    # 2. Place Sell Order
    elif menu == "Place Sell Order":
        st.subheader("💸 Place Sell Order")

        market = st.text_input("Market (e.g., BTCUSDT)", "BTCUSDT")
        order_type = st.selectbox("Order Type", ["Market Order", "Limit Order"])
        quantity = st.number_input("Quantity to Sell", min_value=0.0001, step=0.0001)
        price = None

        if order_type == "Limit Order":
            price = st.number_input("Limit Price", min_value=0.01, step=0.01)

        place_order_button = st.button("Place Sell Order")
        
        if place_order_button:
            try:
                if order_type == "Market Order":
                    response = app.order_service.place_market_order(
                        market=market,
                        side="sell",
                        quantity=quantity,
                        user_id=st.session_state["user_id"]
                    )
                    st.success(f"✅ Market Sell Order placed! Quantity: {quantity}, Response: {response}")
                elif order_type == "Limit Order" and price:
                    response = app.order_service.place_limit_order(
                        market=market,
                        side="sell",
                        quantity=quantity,
                        price=price,
                        user_id=st.session_state["user_id"]
                    )
                    st.success(f"✅ Limit Sell Order placed! Quantity: {quantity}, Price: {price}, Response: {response}")
                else:
                    st.error("❌ Limit price is required for limit orders.")
            except Exception as e:
                st.error(f"Error placing sell order: {e}")
            

    # 3. View Active Orders
    elif menu == "View Active Orders":
        st.subheader("📃 Active Orders")
        try:
            active_orders = app.order_service.get_active_orders(user_id=st.session_state["user_id"])
            if not active_orders:
                st.info("No active orders.")
            else:
                orders_df = pd.DataFrame(active_orders)
                st.dataframe(orders_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching active orders: {e}")

    # 4. Cancel Order
    elif menu == "Cancel Order":
        st.subheader("❌ Cancel Order")
        try:
            active_orders = app.order_service.get_active_orders(user_id=st.session_state["user_id"])
            if not active_orders:
                st.info("No active orders to cancel.")
            else:
                orders_df = pd.DataFrame(active_orders)
                st.dataframe(orders_df, use_container_width=True)

                order_id = st.text_input("Enter Order ID to cancel:")
                cancel_button = st.button("Cancel Order")
                
                if cancel_button and order_id:
                    try:
                        response = app.order_service.cancel_order(order_id, user_id=st.session_state["user_id"])
                        st.success(f"✅ Order {order_id} canceled successfully! Response: {response}")
                    except Exception as e:
                        st.error(f"Error canceling order: {e}")
                elif cancel_button and not order_id:
                    st.warning("Please enter an Order ID to cancel.")
        except Exception as e:
            st.error(f"Error fetching active orders: {e}")

    # 5. View Order History
    elif menu == "View Order History":
        st.subheader("📜 Order History")
        try:
            order_history = app.order_service.get_order_history(user_id=st.session_state["user_id"])
            if not order_history:
                st.info("No order history available.")
            else:
                history_df = pd.DataFrame(order_history)
                st.dataframe(history_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching order history: {e}")

# 6. Agent Analysis
    elif menu == "Agent Analysis":
        st.subheader("🤖 Agent Analysis")
        try:
            # Get market for analysis
            market = st.text_input("Market to analyze (e.g., BTCUSDT)", "BTCUSDT")
            timeframe = st.selectbox("Timeframe", ["1h", "4h", "1d", "1w"])
            
            if st.button("Run Analysis"):
                # Placeholder for calling the analysis service
                st.info("Running market analysis...")
                
                # Initialize simulated agents
                class SimulatedTradingAgent:
                    def __init__(self, name, role, goal, backstory):
                        self.name = name
                        self.role = role
                        self.goal = goal
                        self.backstory = backstory

                    def analyze_market(self, market_data):
                        """Analyze market data for BTC/USDT. Assumes `market_data` is a list of dictionaries."""
                        try:
                            prices = [float(item.get("last_price", 0)) for item in market_data if item.get("last_price")]
                            if not prices:
                                return f"{self.name}: Insufficient data to analyze."
                            
                            avg_price = sum(prices) / len(prices)
                            current_price = prices[-1]
                            
                            if current_price > avg_price:
                                return f"{self.name}: Bullish trend detected – current price {current_price} is above average {avg_price:.2f}."
                            else:
                                return f"{self.name}: Bearish trend detected – current price {current_price} is below average {avg_price:.2f}."
                        except Exception as e:
                            return f"{self.name}: Error in market analysis: {str(e)}"

                    def advise_trade(self, market_analysis, balance_data):
                        """Advise trades based on market trends."""
                        if "Bullish" in market_analysis:
                            return f"{self.name}: Advice - Consider buying."
                        elif "Bearish" in market_analysis:
                            return f"{self.name}: Advice - Consider selling."
                        else:
                            return f"{self.name}: Advice - Hold your current positions."

                # Create agent instances
                market_agent = SimulatedTradingAgent(
                    name="Crypto Analyst Alpha",
                    role="Market Analyst",
                    goal="Analyze market trends for BTC/USDT",
                    backstory="Expert in crypto market analysis."
                )

                trade_agent = SimulatedTradingAgent(
                    name="Trade Advisor Beta",
                    role="Trade Advisor",
                    goal="Advise trades based on market trends and balance",
                    backstory="Experienced in managing portfolios and advising trades."
                )

                # Example market data for analysis
                market_data = [
                    {"symbol": "BTCUSDT", "last_price": 60000},
                    {"symbol": "BTCUSDT", "last_price": 61000},
                    {"symbol": "BTCUSDT", "last_price": 59500},
                    {"symbol": "BTCUSDT", "last_price": 63000},
                ]

                # Perform analysis using the agents
                market_analysis = market_agent.analyze_market(market_data)
                st.write(f"Market Analysis by {market_agent.name}: {market_analysis}")
                
                # Example balance data (can be dynamically fetched from user's portfolio or trading data)
                balance_data = {"BTC": 0.1, "USDT": 1000}
                trade_advice = trade_agent.advise_trade(market_analysis, balance_data)
                st.write(f"Trade Advice by {trade_agent.name}: {trade_advice}")
                
                # Placeholder for displaying results
                st.subheader("Analysis Results")
                st.write("Market trend: Bullish")
                st.write("Support levels: $40,000, $38,500")
                st.write("Resistance levels: $42,000, $44,000")
                
                # You could also display charts
                st.subheader("Market Chart")
                st.line_chart({"price": [41000, 41200, 41500, 41300, 41600, 41800, 42000]})
                
                # And recommendations
                st.subheader("Recommendations")
                st.write("Consider placing limit buy orders at support levels.")
                st.write("Target taking profits near resistance levels.")
        except Exception as e:
            # Initialize FAISS vector database
            st.subheader("🔍 FAISS Vector Database")

            # Load or create FAISS index
            index_file = "faiss_index.bin"
            dimension = 768  # Assuming embeddings are 768-dimensional
            model = SentenceTransformer('all-MiniLM-L6-v2')  # Load a pre-trained model for embeddings

            if os.path.exists(index_file):
                index = faiss.read_index(index_file)
                st.success("✅ FAISS index loaded successfully.")
            else:
                index = faiss.IndexFlatL2(dimension)
                st.info("ℹ️ New FAISS index created.")

            # Add data to FAISS index
            if st.button("Add Data to FAISS Index"):
                try:
                    data = st.text_area("Enter data to add (one entry per line):")
                    if data.strip():
                        entries = data.split("\n")
                        embeddings = model.encode(entries)
                        index.add(embeddings)
                        faiss.write_index(index, index_file)
                        st.success(f"✅ Added {len(entries)} entries to FAISS index.")
                    else:
                        st.warning("Please enter some data to add.")
                except Exception as e:
                    st.error(f"Error adding data to FAISS index: {e}")

            # Search FAISS index
            if st.button("Search FAISS Index"):
                try:
                    query = st.text_input("Enter search query:")
                    if query.strip():
                        query_embedding = model.encode([query])
                        distances, indices = index.search(query_embedding, k=5)  # Retrieve top 5 results
                        st.write("Search Results:")
                        for i, idx in enumerate(indices[0]):
                            st.write(f"{i + 1}. Index: {idx}, Distance: {distances[0][i]}")
                    else:
                        st.warning("Please enter a search query.")
                except Exception as e:
                    st.error(f"Error searching FAISS index: {e}")
