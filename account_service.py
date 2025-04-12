# account_service.py
from typing import Dict, List
import pandas as pd
from redis_cache import cache_data, get_cached_data


class AccountService:
    """
    Service for handling account-related operations.
    """
    
    def __init__(self, api_service, market_service):
        """
        Initialize the account service.
        
        Args:
            api_service: An instance of CoinDCXApiService
            market_service: An instance of MarketService
        """
        self.api_service = api_service
        self.market_service = market_service
    
    def get_account_balance(self, user_id=None):
        cache_key = f"balance:{user_id}" if user_id else "balance:global"
    
        cached = get_cached_data(cache_key)
        if cached:
            return cached

        endpoint = "/exchange/v1/users/balances"
        result = self.api_service.make_authenticated_request(endpoint,{})
        
        if user_id:
            cache_data(cache_key, result, ttl=300)  # Cache for 5 minutes
        return result
    
    def display_portfolio(self) -> None:
        """
        Display user portfolio with current values.
        """
        balances = self.get_account_balance()
        ticker_data = {item['market']: item for item in self.market_service.get_ticker_data()}
        
        portfolio = []
        
        for balance in balances:
            if float(balance['balance']) > 0:
                coin = balance['currency']
                holding = {
                    'Coin': coin,
                    'Balance': float(balance['balance']),
                    'Locked': float(balance.get('locked_balance', 0)),
                }
                
                # Try to calculate INR value for the coin
                try:
                    market = f"{coin}INR"
                    if market in ticker_data:
                        price = float(ticker_data[market]['last_price'])
                        holding['Price (INR)'] = price
                        holding['Value (INR)'] = price * holding['Balance']
                except:
                    # Skip if we can't find a direct INR pair
                    holding['Price (INR)'] = 'N/A'
                    holding['Value (INR)'] = 'N/A'
                
                portfolio.append(holding)
        
        # Convert to DataFrame and display
        df = pd.DataFrame(portfolio)
        print("\n=== Your Portfolio ===")
        print(df.to_string(index=False))
        
        # Calculate total portfolio value
        try:
            total_value = sum([h['Value (INR)'] for h in portfolio if isinstance(h['Value (INR)'], (int, float))])
            print(f"\nTotal Portfolio Value: ₹{total_value:.2f}")
        except:
            pass
    
    def get_deposit_history(self) -> List[Dict]:
        """
        Get deposit history.
        
        Returns:
            List of deposit transactions
        """
        endpoint = "/v1/exchange/users/deposit_history"
        body = {}
        return self.api_service.make_authenticated_request(endpoint, body)
    
    def get_withdrawal_history(self) -> List[Dict]:
        """
        Get withdrawal history.
        
        Returns:
            List of withdrawal transactions
        """
        endpoint = "/v1/exchange/users/withdrawal_history"
        body = {}
        return self.api_service.make_authenticated_request(endpoint, body)