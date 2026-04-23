"""Order placement and management logic"""
import logging
from typing import Dict, Any, Optional
from .client import BinanceFuturesClient
from .validators import *

logger = logging.getLogger(__name__)

class OrderManager:
    """Manages order placement and validation"""
    
    def __init__(self, client: BinanceFuturesClient):
        """Initialize order manager with client"""
        self.client = client
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Validate and place an order"""
        
        # Validate all inputs
        is_valid, symbol = validate_symbol(symbol)
        if not is_valid:
            raise ValueError(f"Invalid symbol: {symbol}")
        
        is_valid, side = validate_side(side)
        if not is_valid:
            raise ValueError(f"Invalid side: {side}")
        
        is_valid, order_type = validate_order_type(order_type)
        if not is_valid:
            raise ValueError(f"Invalid order type: {order_type}")
        
        is_valid, quantity = validate_quantity(quantity)
        if not is_valid:
            raise ValueError(f"Invalid quantity: {quantity}")
        
        is_valid, price = validate_price(price, order_type)
        if not is_valid:
            raise ValueError(f"Invalid price: {price}")
        
        # Get current price for logging (optional)
        if order_type == 'MARKET':
            current_price = self.client.get_symbol_price(symbol)
            logger.info(f"Current market price for {symbol}: {current_price}")
        
        # Place the order
        order = self.client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        return order
    
    def format_order_summary(self, order: Dict[str, Any]) -> str:
        """Format order response for display"""
        summary = f"""
Order Summary:
  Order ID: {order.get('orderId', 'N/A')}
  Symbol: {order.get('symbol', 'N/A')}
  Side: {order.get('side', 'N/A')}
  Type: {order.get('type', 'N/A')}
  Quantity: {order.get('origQty', 'N/A')}
  Status: {order.get('status', 'N/A')}
  Executed Qty: {order.get('executedQty', '0')}
  Avg Price: {order.get('avgPrice', 'N/A')}
  Price: {order.get('price', 'N/A') if order.get('price') != '0' else 'Market'}
"""
        return summary
    

    def place_stop_limit_order(
    self,
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
    limit_price: float
) -> Dict[str, Any]:
        """Place a stop-limit order"""
        try:
            side = side.upper()
        
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce='GTC'
        )
        
            logger.info(f"Stop-limit order placed: {order}")
            return order
        
        except Exception as e:
            logger.error(f"Failed to place stop-limit order: {e}")
            raise