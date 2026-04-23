"""Input validation for trading bot"""
import re
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

# Common trading pairs on Binance Futures
VALID_SYMBOLS = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'DOGEUSDT', 'ADAUSDT', 'MATICUSDT', 'LINKUSDT', 
    'DOTUSDT', 'AVAXUSDT', 'NEARUSDT', 'ATOMUSDT', 'UNIUSDT', 'AAVEUSDT', 'FILUSDT','LTCUSDT', 'BCHUSDT', 
    'ETCUSDT', 'XLMUSDT', 'VETUSDT', 'ALGOUSDT', 'SANDUSDT', 'MANAUSDT', 'ENJUSDT'
]

def validate_symbol(symbol: str) -> Tuple[bool, str]:
    """Validate trading symbol"""
    symbol = symbol.upper()
    
    if not symbol:
        return False, "Symbol cannot be empty"
    
    if not re.match(r'^[A-Z]+USDT$', symbol):
        return False, "Symbol must end with USDT (e.g., BTCUSDT)"
    
    # Optional: check against valid symbols list
    if symbol not in VALID_SYMBOLS:
        logger.warning(f"Symbol {symbol} not in common list, but will attempt to use")
    
    return True, symbol

def validate_side(side: str) -> Tuple[bool, str]:
    """Validate order side"""
    side = side.upper()
    
    if side not in ['BUY', 'SELL']:
        return False, "Side must be either BUY or SELL"
    
    return True, side

def validate_order_type(order_type: str) -> Tuple[bool, str]:
    """Validate order type"""
    order_type = order_type.upper()
    
    if order_type not in ['MARKET', 'LIMIT']:
        return False, "Order type must be either MARKET or LIMIT"
    
    return True, order_type

def validate_quantity(quantity: float, symbol: str = None) -> Tuple[bool, str]:
    """Validate order quantity"""
    try:
        quantity = float(quantity)
    except (ValueError, TypeError):
        return False, "Quantity must be a valid number"
    
    if quantity <= 0:
        return False, "Quantity must be greater than 0"
    
    if quantity > 1000:  # Reasonable max for testnet
        logger.warning(f"Large quantity detected: {quantity}")
    
    return True, quantity

def validate_price(price: float, order_type: str) -> Tuple[bool, str]:
    """Validate price (required for LIMIT orders)"""
    if order_type.upper() == 'MARKET':
        return True, None
    
    try:
        price = float(price)
    except (ValueError, TypeError):
        return False, "Price must be a valid number"
    
    if price <= 0:
        return False, "Price must be greater than 0"
    
    return True, price


def validate_order_with_market(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    current_price: float = None
) -> Tuple[bool, str]:
    """Validate order with market context"""
    
    if current_price:
        if order_type == 'LIMIT':
            if side == 'BUY' and price > current_price * 1.1:
                return False, f"Limit buy price {price} is 10% above market {current_price}"
            elif side == 'SELL' and price < current_price * 0.9:
                return False, f"Limit sell price {price} is 10% below market {current_price}"
    
    return True, "Valid"