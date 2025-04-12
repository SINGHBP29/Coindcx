# main.py
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Import services
from api_service import CoinDCXApiService
from market_service import MarketService
from account_service import AccountService
from order_service import OrderService

class TradingApp:
    """
    Main application class for CoinDCX Trading Platform.
    Integrates all microservices and provides a user interface.
    """
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the trading application with all required services.
        
        Args:
            api_key: CoinDCX API key
            api_secret: CoinDCX API secret
        """
        # Initialize services
        self.api_service = CoinDCXApiService(api_key, api_secret)
        self.market_service = MarketService()
        self.account_service = AccountService(self.api_service, self.market_service)
        self.order_service = OrderService(self.api_service)
        # self.market_service = MarketService()
        # self.account_service = AccountService(api_key, api_secret)
        # self.order_service = OrderService(api_key, api_secret)
    
        
    def main_menu(self) -> None:
        """
        Display and handle the main menu.
        """
        while True:
            print("\n==== CoinDCX Trading Platform ====")
            print("1. View Market Data")
            print("2. View Portfolio")
            print("3. Place Buy Order")
            print("4. Place Sell Order")
            print("5. View Active Orders")
            print("6. Cancel Order")
            print("7. View Order History")
            print("0. Exit")
            
            choice = input("\nEnter your choice: ")
            
            try:
                if choice == '1':
                    self._view_market_data()
                elif choice == '2':
                    self._view_portfolio()
                elif choice == '3':
                    self._place_order("buy")
                elif choice == '4':
                    self._place_order("sell")
                elif choice == '5':
                    self._view_active_orders()
                elif choice == '6':
                    self._cancel_order()
                elif choice == '7':
                    self._view_order_history()
                elif choice == '0':
                    print("Thank you for using CoinDCX Trading Platform!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {str(e)}")
                
    def _view_market_data(self) -> None:
        """
        View market data with filtering option.
        """
        filter_market = input("Enter market to filter (e.g., BTC, ETH) or leave blank for all: ")
        self.market_service.display_ticker_table(filter_market)
        
    def _view_portfolio(self) -> None:
        """
        View user portfolio.
        """
        self.account_service.display_portfolio()
        
    def _place_order(self, side: str) -> None:
        """
        Place a buy or sell order.
        
        Args:
            side: Order side ("buy" or "sell")
        """
        print(f"\n==== Place {side.capitalize()} Order ====")
        
        market = input("Enter market (e.g., BTCINR): ").upper()
        order_type = input("Order type (1: Limit, 2: Market): ")
        
        quantity = float(input("Enter quantity: "))
        
        if order_type == '1':
            price = float(input("Enter price: "))
            response = self.order_service.place_limit_order(market, side, price, quantity)
            print(f"\n{side.capitalize()} limit order placed successfully!")
        elif order_type == '2':
            response = self.order_service.place_market_order(market, side, quantity)
            print(f"\n{side.capitalize()} market order placed successfully!")
        else:
            print("Invalid order type!")
            return
            
        print(f"Order ID: {response.get('id', 'N/A')}")
        print(f"Status: {response.get('status', 'N/A')}")
        
    def _view_active_orders(self) -> None:
        """
        View all active orders.
        """
        self.order_service.display_active_orders()
            
    def _cancel_order(self) -> None:
        """
        Cancel an active order.
        """
        order_id = input("\nEnter Order ID to cancel: ")
        response = self.order_service.cancel_order(order_id)
        print(f"\nOrder {order_id} canceled successfully!")
        
    def _view_order_history(self) -> None:
        """
        View order history.
        """
        self.order_service.display_order_history()
    




def load_credentials():
    """
    Load API credentials from .env file.
    
    Returns:
        tuple: (api_key, api_secret)
    """
    # Try to load from .env file
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    api_key = os.getenv("COINDCX_API_KEY")
    api_secret = os.getenv("COINDCX_API_SECRET")
    
    # Check if credentials were loaded successfully
    if not api_key or not api_secret:
        print("ERROR: API credentials not found in .env file.")
        print("Please create a .env file with your CoinDCX API credentials:")
        print("COINDCX_API_KEY=your_api_key_here")
        print("COINDCX_API_SECRET=your_api_secret_here")
        sys.exit(1)
    
    return api_key, api_secret


# Example usage
if __name__ == "__main__":
    print("Welcome to the CoinDCX Trading Platform!")
    
    # Load API credentials from .env file
    api_key, api_secret = load_credentials()
    print("API credentials loaded successfully from .env file.")
    
    # Initialize and run the trading app
    app = TradingApp(api_key, api_secret)
    app.main_menu()