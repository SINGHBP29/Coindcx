# from api_service import CoinDCXApiService
from main import load_credentials
from api_service import CoinDCXApiService

api_key, api_secret = load_credentials()
coindcx = CoinDCXApiService(api_key, api_secret)
# Initialize your CoinDCX API client
# coindcx = CoinDCXApiService()

# Fetch market data and balance data
market_data = coindcx.get_ticker_data(symbol="BTCUSDT")
balance_data = coindcx.get_balance()

# Define a simulated trading agent class with a name attribute
class SimulatedTradingAgent:
    def __init__(self, name, role, goal, backstory):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def analyze_market(self, market_data):
        """
        Analyze market data for BTC/USDT. Assumes `market_data` is a list of dictionaries,
        each with a 'last_price' key.
        """
        try:
            # Extract prices from market data
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
        """
        Provide a trade recommendation based on the market analysis.
        For simplicity, returns a buy recommendation if the analysis is bullish,
        and a sell recommendation if bearish.
        """
        if "Bullish" in market_analysis:
            return f"{self.name}: Advice - Consider buying."
        elif "Bearish" in market_analysis:
            return f"{self.name}: Advice - Consider selling."
        else:
            return f"{self.name}: Advice - Hold your current positions."

# Create instances of the simulated agents with specific names
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
    backstory="Veteran trading strategist."
)

# Execute agent functions to produce output
market_analysis = market_agent.analyze_market(market_data)
trade_recommendation = trade_agent.advise_trade(market_analysis, balance_data)

# Print out the results
print("Market Analysis:")
print(market_analysis)
print("\nTrade Recommendation:")
print(trade_recommendation)
