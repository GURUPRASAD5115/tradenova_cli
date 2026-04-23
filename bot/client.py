"""Binance Futures client wrapper"""
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance.enums import FUTURE_ORDER_TYPE_LIMIT, FUTURE_ORDER_TYPE_MARKET
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    """Wrapper for Binance Futures Testnet API"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """Initialize the Binance Futures client"""
        self.api_key = api_key
        self.api_secret = api_secret
        
        try:
            # Initialize client for futures testnet
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet
            )
            
            # Enable futures trading
            self.client.futures_account()
            logger.info("Binance Futures client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get futures account information"""
        try:
            account_info = self.client.futures_account()
            logger.debug(f"Account info retrieved: {account_info}")
            return account_info
        except BinanceAPIException as e:
            logger.error(f"API error getting account info: {e}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Network error getting account info: {e}")
            raise
    
    def get_symbol_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.debug(f"Current price for {symbol}: {price}")
            return price
        except Exception as e:
            logger.error(f"Failed to get price for {symbol}: {e}")
            raise
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Place a futures order"""
        try:
            # Convert side to Binance format
            side = side.upper()
            order_type = order_type.upper()
            
            # Prepare order parameters
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }
            
            # Add price for limit orders
            if order_type == 'LIMIT':
                if not price:
                    raise ValueError("Price is required for LIMIT orders")
                order_params['price'] = str(price)
                order_params['timeInForce'] = 'GTC'  # Good Till Canceled
            
            logger.info(f"Placing order: {order_params}")
            
            # Execute order based on type
            if order_type == 'MARKET':
                order = self.client.futures_create_order(**order_params)
            elif order_type == 'LIMIT':
                order = self.client.futures_create_order(**order_params)
            else:
                raise ValueError(f"Unsupported order type: {order_type}")
            
            logger.info(f"Order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing order: {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Network error placing order: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Get status of a specific order"""
        try:
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            logger.debug(f"Order status: {order}")
            return order
        except Exception as e:
            logger.error(f"Failed to get order status: {e}")
            raise

    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """Get all open orders"""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol)
            else:
                orders = self.client.futures_get_open_orders()
            return orders
        except Exception as e:
            logger.error(f"Failed to get open orders: {e}")
            return []

    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel a specific order"""
        try:
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            logger.info(f"Order {order_id} cancelled")
            return result
        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            raise

    def get_balance_summary(self) -> Dict:
        """Get formatted balance summary"""
        try:
            account = self.futures_account()
            balances = {}
            for asset in account['assets']:
                if float(asset['walletBalance']) > 0:
                    balances[asset['asset']] = {
                    'wallet': float(asset['walletBalance']),
                    'available': float(asset['availableBalance'])
                }
            return balances
        except Exception as e:
            logger.error(f"Failed to get balances: {e}")
            return {}