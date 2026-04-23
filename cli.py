#!/usr/bin/env python3
"""CLI interface for the trading bot"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add bot module to path
sys.path.insert(0, str(Path(__file__).parent))

from bot.logging_config import setup_logging, get_logger
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Trading Bot for Binance Futures Testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Market BUY order
  python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
  
  # Limit SELL order
  python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 2000
  
  # Interactive mode
  python cli.py --interactive
        """
    )
    
    parser.add_argument(
        '--symbol',
        type=str,
        help='Trading symbol (e.g., BTCUSDT)'
    )
    
    parser.add_argument(
        '--side',
        type=str,
        choices=['BUY', 'SELL'],
        help='Order side: BUY or SELL'
    )
    
    parser.add_argument(
        '--order-type',  # Changed from --type to --order-type
        type=str,
        choices=['MARKET', 'LIMIT'],
        help='Order type: MARKET or LIMIT'
    )
    
    parser.add_argument(
        '--quantity',
        type=float,
        help='Order quantity'
    )
    
    parser.add_argument(
        '--price',
        type=float,
        help='Price for LIMIT orders (required if order-type is LIMIT)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='Binance API Key (or set BINANCE_API_KEY env var)'
    )
    
    parser.add_argument(
        '--api-secret',
        type=str,
        help='Binance API Secret (or set BINANCE_API_SECRET env var)'
    )
    
    return parser.parse_args()

def interactive_mode(order_manager: OrderManager):
    """Run the bot in interactive mode"""
    print("\n" + "="*50)
    print("🤖 Trading Bot - Interactive Mode")
    print("="*50)
    
    while True:
        print("\n📋 Order Details:")
        
        # Get symbol
        while True:
            symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
            if symbol:
                break
            print("❌ Symbol cannot be empty")
        
        # Get side
        while True:
            side = input("Side (BUY/SELL): ").strip().upper()
            if side in ['BUY', 'SELL']:
                break
            print("❌ Side must be BUY or SELL")
        
        # Get order type
        while True:
            order_type = input("Order Type (MARKET/LIMIT): ").strip().upper()
            if order_type in ['MARKET', 'LIMIT']:
                break
            print("❌ Order type must be MARKET or LIMIT")
        
        # Get quantity
        while True:
            try:
                quantity = float(input("Quantity: ").strip())
                if quantity > 0:
                    break
                print("❌ Quantity must be greater than 0")
            except ValueError:
                print("❌ Invalid quantity")
        
        # Get price for limit orders
        price = None
        if order_type == 'LIMIT':
            while True:
                try:
                    price = float(input("Price: ").strip())
                    if price > 0:
                        break
                    print("❌ Price must be greater than 0")
                except ValueError:
                    print("❌ Invalid price")
        
        # Display order summary
        print("\n" + "-"*50)
        print("📝 Order Summary:")
        print(f"  Symbol: {symbol}")
        print(f"  Side: {side}")
        print(f"  Type: {order_type}")
        print(f"  Quantity: {quantity}")
        if price:
            print(f"  Price: {price}")
        print("-"*50)
        
        # Confirm order
        confirm = input("\nConfirm order? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("❌ Order cancelled")
            continue
        
        # Place order
        try:
            order = order_manager.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )
            
            print("\n✅ ORDER SUCCESSFUL!")
            print(order_manager.format_order_summary(order))
            
            # Ask to continue
            again = input("\nPlace another order? (yes/no): ").strip().lower()
            if again not in ['yes', 'y']:
                print("\n👋 Goodbye!")
                break
                
        except Exception as e:
            print(f"\n❌ ORDER FAILED: {e}")
            logger.error(f"Order placement failed: {e}")

def main():
    """Main entry point"""
    print("\n🚀 Trading Bot - Binance Futures Testnet")
    print("="*50)
    
    # Parse arguments
    args = parse_arguments()
    
    # Get API credentials
    api_key = args.api_key or os.getenv('BINANCE_API_KEY')
    api_secret = args.api_secret or os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("\n❌ ERROR: API credentials not found!")
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
        print("Or use --api-key and --api-secret arguments")
        print("\nExample:")
        print("  export BINANCE_API_KEY=your_key")
        print("  export BINANCE_API_SECRET=your_secret")
        sys.exit(1)
    
    try:
        # Initialize client
        print("\n🔌 Connecting to Binance Futures Testnet...")
        client = BinanceFuturesClient(api_key, api_secret, testnet=True)
        
        # Get account info to verify connection
        account_info = client.get_account_info()
        print(f"✅ Connected successfully!")
        print(f"📊 Account Balance: {float(account_info['totalWalletBalance']):.2f} USDT")
        
        # Initialize order manager
        order_manager = OrderManager(client)
        
        # Interactive mode or single order
        if args.interactive:
            interactive_mode(order_manager)
        else:
            # Validate required arguments for single order
            if not all([args.symbol, args.side, args.order_type, args.quantity]):
                print("\n❌ ERROR: Missing required arguments for single order")
                print("Required: --symbol, --side, --order-type, --quantity")
                print("For LIMIT orders, also required: --price")
                print("\nUse --help for usage information or --interactive for guided mode")
                sys.exit(1)
            
            # Validate price for limit orders
            if args.order_type == 'LIMIT' and not args.price:
                print("\n❌ ERROR: --price is required for LIMIT orders")
                sys.exit(1)
            
            # Place single order
            print(f"\n📝 Placing {args.order_type} {args.side} order for {args.quantity} {args.symbol}...")
            
            order = order_manager.place_order(
                symbol=args.symbol,
                side=args.side,
                order_type=args.order_type,
                quantity=args.quantity,
                price=args.price
            )
            
            print("\n✅ ORDER SUCCESSFUL!")
            print(order_manager.format_order_summary(order))
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Bot stopped by user")
        logger.info("Bot stopped by user")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()