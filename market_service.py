# market_service.py
from typing import Dict, List, Optional
import pandas as pd
import requests
from datetime import datetime

class MarketService:
    """
    Service for handling market data and operations.
    """
    
    def __init__(self, api_service):
        """
        Initialize the market service.
        
        Args:
            api_service: An instance of CoinDCXApiService
        """
        self.api_service = api_service
    
    def __init__(self):
        self.api_url = "https://api.coindcx.com/exchange/ticker"

    def get_ticker_dataframe(self, filter_market=""):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data)
            df = df[df['market'].str.endswith("INR")]

            if filter_market:
                filter_market = filter_market.upper()
                df = df[df['market'].str.contains(filter_market)]

            df = df[["market", "last_price", "high", "low", "volume", "change_24_hour"]]
            df.columns = ["Market", "Last Price", "High", "Low", "Volume", "Change %"]

            return df

        except Exception as e:
            print(f"[ERROR] Market data fetch failed: {e}")
            return pd.DataFrame()
        
    # def get_ticker_dataframe(self, filter_market=""):
    #     try:
    #         response = requests.get(self.api_url)
    #         data = response.json()

    #         # Filter to only INR markets (or others if needed)
    #         df = pd.DataFrame(data)
    #         df = df[df['market'].str.endswith("INR")]

    #         # Optional: filter by coin name
    #         if filter_market:
    #             filter_market = filter_market.upper()
    #             df = df[df['market'].str.contains(filter_market)]

    #         # Select and rename relevant columns
    #         df = df[["market", "last_price", "high", "low", "volume", "change_24_hour"]]
    #         df.columns = ["Market", "Last Price", "High", "Low", "Volume", "Change %"]

    #         return df

    #     except Exception as e:
    #         print(f"[ERROR] Market data fetch failed: {e}")
    #         return pd.DataFrame()
        
    def get_market_data(self) -> List[Dict]:
        """
        Get market data for all trading pairs.
        
        Returns:
            List of market data for all trading pairs
        """
        endpoint = "/exchange/v1/markets"
        return self.api_service.make_public_request(endpoint)
    
    def get_ticker_data(self) -> Dict:
        """
        Get ticker data for all symbols.
        
        Returns:
            Dictionary of ticker data
        """
        endpoint = "/exchange/ticker"
        return self.api_service.make_public_request(endpoint)
    
    # def display_ticker_table(self, filter_market: Optional[str] = None) -> None:
    #     """
    #     Display ticker data in a formatted table.
        
    #     Args:
    #         filter_market: Optionally filter by market (e.g., "BTC", "ETH")
    #     """
    #     ticker_data = self.get_ticker_data()
        
    #     # Convert to DataFrame for easier manipulation
    #     df = pd.DataFrame(ticker_data)
        
    #     # Filter if needed
    #     if filter_market:
    #         df = df[df['market'].str.contains(filter_market, case=False)]
        
    #     # Select and rename columns for display
    #     display_df = df[['market', 'last_price', 'high', 'low', 'volume', 'change_24_hour']].copy()
    #     display_df.columns = ['Market', 'Last Price', 'High', 'Low', 'Volume', '24h Change (%)']
        
    #     # Format the change column
    #     display_df['24h Change (%)'] = display_df['24h Change (%)'].astype(float).map('{:.2f}%'.format)
        
    #     # Print the table
    #     print(display_df.to_string(index=False))
    
    def display_ticker_table(self, filter_market: Optional[str] = None) -> None:
        """
        Display ticker data in a formatted table.
        
        Args:
            filter_market: Optionally filter by market (e.g., "BTC", "ETH")
        """
        ticker_data = self.get_ticker_data()
        
        df = pd.DataFrame(ticker_data)

        if df.empty:
            print("No ticker data available.")
            return

        if filter_market:
            df = df[df['market'].str.contains(filter_market, case=False)]

        try:
            # Select and rename columns
            display_df = df[['market', 'last_price', 'high', 'low', 'volume', 'change_24_hour']].copy()
            display_df.columns = ['Market', 'Last Price', 'High', 'Low', 'Volume', '24h Change (%)']

            # Convert to float safely
            display_df['24h Change (%)'] = pd.to_numeric(display_df['24h Change (%)'], errors='coerce')
            display_df['24h Change (%)'] = display_df['24h Change (%)'].map(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")

            print(display_df.to_string(index=False))

        except KeyError as e:
            print(f"[ERROR] Missing expected column in API response: {e}")
        except Exception as e:
            print(f"[ERROR] Failed to process ticker table: {e}")

    
    def get_order_book(self, market: str) -> Dict:
        """
        Get the order book for a specific market.
        
        Args:
            market: Market identifier (e.g., "BTCINR")
            
        Returns:
            Order book data
        """
        endpoint = "/market_data/orderbook"
        params = {"pair": market}
        return self.api_service.make_public_request(endpoint, params=params)
    
    def get_trade_history(self, market: str) -> List[Dict]:
        """
        Get recent trades for a specific market.
        
        Args:
            market: Market identifier (e.g., "BTCINR")
            
        Returns:
            Recent trade data
        """
        endpoint = "/market_data/trade_history"
        params = {"pair": market}
        return self.api_service.make_public_request(endpoint, params=params)
    

    # def get_ticker_dataframe(self, filter_market=""):
    #     endpoint = "/exchange/ticker"
    #     response = self.api_service.make_public_request(endpoint)

    #     df = pd.DataFrame(response)

    #     # Filter if needed
    #     if filter_market:
    #         df = df[df['market'].str.contains(filter_market.upper())]

    #     # Select relevant columns
    #     df = df[["market", "last_price", "high", "low", "volume"]]
    #     df = df.sort_values("volume", ascending=False).reset_index(drop=True)
    #     return df
