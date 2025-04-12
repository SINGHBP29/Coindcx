import time
from typing import Dict, List
from datetime import datetime
from redis_cache import cache_data, get_cached_data, append_to_cache_list

class OrderService:
    """
    Service for handling order-related operations.
    """
    
    def __init__(self, api_service):
        """
        Initialize the order service.
        
        Args:
            api_service: An instance of CoinDCXApiService
        """
        self.api_service = api_service
    
    def place_limit_order(
        self, 
        market: str,
        side: str, 
        price: float, 
        quantity: float,
        user_id=None
    ) -> Dict:
        """
        Place a limit order.
        """
        # Updated endpoint to match CoinDCX API
        endpoint = "/exchange/v1/orders/create"
        
        body = {
            "side": side.lower(),  # buy or sell
            "order_type": "limit_order",
            "market": market,
            "price_per_unit": float(price),
            "total_quantity": float(quantity),
            "timestamp": int(time.time() * 1000),
            "client_order_id": f"coindcx_{int(time.time() * 1000)}"
        }
        
        response = self.api_service.make_authenticated_request(endpoint, body)
        if user_id:
            append_to_cache_list(f"order_history:{user_id}", response)
        return response
    
    def place_market_order(
        self, 
        market: str,
        side: str, 
        quantity: float,
        user_id=None
    ) -> Dict:
        """
        Place a market order.
        """
        # Updated endpoint to match CoinDCX API
        endpoint = "/exchange/v1/orders/create"
        
        body = {
            "side": side.lower(),  # buy or sell
            "order_type": "market_order",
            "market": market,
            "total_quantity": float(quantity),
            "timestamp": int(time.time() * 1000),
            "client_order_id": f"coindcx_{int(time.time() * 1000)}"
        }
        
        response = self.api_service.make_authenticated_request(endpoint, body)
        if user_id:
            append_to_cache_list(f"order_history:{user_id}", response)
        return response
   
    def cancel_order(self, order_id: str, user_id=None) -> Dict:
        """
        Cancel an active order.
        """
        # Updated endpoint to match CoinDCX API
        endpoint = "/exchange/v1/orders/cancel"
        
        body = {
            "id": order_id,
            "timestamp": int(time.time() * 1000)
        }
        
        response = self.api_service.make_authenticated_request(endpoint, body)
        return response
    
    def get_active_orders(self, user_id=None):
        """
        Get active orders (with Redis caching).
        """
        cache_key = f"active_orders:{user_id}" if user_id else "active_orders:global"
        cached = get_cached_data(cache_key)
        if cached:
            return cached

        # Updated endpoint to match CoinDCX API
        endpoint = "/exchange/v1/orders/active_orders"
        
        body = {
            "timestamp": int(time.time() * 1000)
        }
        
        result = self.api_service.make_authenticated_request(endpoint, body)
        
        if user_id:
            cache_data(cache_key, result, ttl=30)  # Cache for 30 seconds
        return result
    
    def get_order_status(self, order_id: str) -> Dict:
        """
        Get the status of a specific order.
        """
        endpoint = "/exchange/v1/orders/status"
        
        body = {
            "id": order_id,
            "timestamp": int(time.time() * 1000)
        }
        
        return self.api_service.make_authenticated_request(endpoint, body)
    
    def get_order_history(self, user_id=None) -> List[Dict]:
        """
        Get order history from API or cache.
        """
        cache_key = f"order_history:{user_id}" if user_id else "order_history:global"
        
        # Try to get from cache first
        cached_history = get_cached_data(cache_key)
        if cached_history:
            return cached_history
            
        # If not in cache, try to get from API
        try:
            endpoint = "/exchange/v1/orders/trade_history"
            body = {
                "timestamp": int(time.time() * 1000)
            }
            
            history = self.api_service.make_authenticated_request(endpoint, body)
            
            # Cache the result
            if user_id:
                cache_data(cache_key, history, ttl=60)  # Cache for 1 minute
                
            return history
        except Exception as e:
            print(f"Failed to get order history: {e}")
            return []
    
    def display_active_orders(self, user_id=None) -> None:
        """
        Display active orders in a formatted way.
        """
        active_orders = self.get_active_orders(user_id)
        
        if not active_orders:
            print("\nNo active orders found.")
            return
            
        print("\n==== Active Orders ====")
        for order in active_orders:
            print(f"ID: {order.get('id')}")
            print(f"Market: {order.get('market')}")
            print(f"Side: {order.get('side')}")
            print(f"Type: {order.get('order_type')}")
            print(f"Price: {order.get('price_per_unit')}")
            print(f"Quantity: {order.get('total_quantity')}")
            print(f"Timestamp: {datetime.fromtimestamp(order.get('timestamp')/1000)}")
            print("-" * 40)
    
    def display_order_history(self, user_id=None) -> None:
        """
        Display order history in a formatted way.
        """
        history = self.get_order_history(user_id)
        
        if not history:
            print("\nNo order history found.")
            return
            
        print("\n==== Order History ====")
        for order in history:
            print(f"ID: {order.get('id')}")
            print(f"Market: {order.get('market')}")
            print(f"Side: {order.get('side')}")
            print(f"Type: {order.get('order_type')}")
            print(f"Price: {order.get('price_per_unit') if 'price_per_unit' in order else 'N/A'}")
            print(f"Quantity: {order.get('total_quantity')}")
            print(f"Status: {order.get('status')}")
            print(f"Timestamp: {datetime.fromtimestamp(order.get('timestamp')/1000)}")
            print("-" * 40)