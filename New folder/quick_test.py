#!/usr/bin/env python3
"""Quick test script for trading bot"""
import os
from dotenv import load_dotenv
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager

load_dotenv()

def test_connection():
    """Test API connection"""
    print("="*50)
    print("TESTING CONNECTION TO BINANCE")
    print("="*50)
    
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ API keys not found!")
        print("\nPlease set your API keys:")
        print("1. Create .env file with:")
        print("   BINANCE_API_KEY=your_key")
        print("   BINANCE_API_SECRET=your_secret")
        return False
    
    print(f"✓ API Key found: {api_key[:10]}...")
    print(f"✓ API Secret found: {api_secret[:10]}...")
    
    try:
        client = BinanceFuturesClient(api_key, api_secret, testnet=True)
        account = client.get_account_info()
        print(f"\n✅ Connected successfully!")
        print(f"💰 Total Balance: {account['totalWalletBalance']} USDT")
        print(f"📊 Available Balance: {account['availableBalance']} USDT")
        return client
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        return False

def test_market_order(client):
    """Test market order"""
    print("\n" + "="*50)
    print("TESTING MARKET ORDER")
    print("="*50)
    order_manager = OrderManager(client)
    
    try:
        print("Placing MARKET BUY order for 0.001 BTCUSDT...")
        order = order_manager.place_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=0.001
        )
        print(f"\n✅ MARKET ORDER SUCCESSFUL!")
        print(f"   Order ID: {order['orderId']}")
        print(f"   Symbol: {order['symbol']}")
        print(f"   Side: {order['side']}")
        print(f"   Type: {order['type']}")
        print(f"   Status: {order['status']}")
        print(f"   Executed Qty: {order.get('executedQty', '0')}")
        return True
    except Exception as e:
        print(f"\n❌ Market order failed: {e}")
        return False

def test_limit_order(client):
    """Test limit order"""
    print("\n" + "="*50)
    print("TESTING LIMIT ORDER")
    print("="*50)
    order_manager = OrderManager(client)
    
    try:
        print("Placing LIMIT SELL order for 0.01 ETHUSDT at price 2500...")
        order = order_manager.place_order(
            symbol="ETHUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity=0.01,
            price=2500
        )
        print(f"\n✅ LIMIT ORDER SUCCESSFUL!")
        print(f"   Order ID: {order['orderId']}")
        print(f"   Symbol: {order['symbol']}")
        print(f"   Side: {order['side']}")
        print(f"   Type: {order['type']}")
        print(f"   Price: {order.get('price', 'N/A')}")
        print(f"   Status: {order['status']}")
        return True
    except Exception as e:
        print(f"\n❌ Limit order failed: {e}")
        return False

def check_logs():
    """Check if log files exist"""
    print("\n" + "="*50)
    print("CHECKING LOG FILES")
    print("="*50)
    
    import glob
    log_files = glob.glob('logs/*.log')
    
    if log_files:
        print(f"✅ Found {len(log_files)} log file(s):")
        for log in log_files:
            print(f"   📄 {log}")
    else:
        print("⚠️  No log files found yet. Run orders first!")

def main():
    """Main test function"""
    print("\n" + "🚀"*25)
    print("   TRADING BOT QUICK TEST SUITE")
    print("🚀"*25)
    
    # Test connection
    client = test_connection()
    if not client:
        print("\n❌ Cannot proceed without API connection")
        return
    
    # Test orders
    print("\n📝 Starting order tests...")
    market_success = test_market_order(client)
    limit_success = test_limit_order(client)
    
    # Check logs
    check_logs()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Connection Test: {'✅ PASS' if client else '❌ FAIL'}")
    print(f"Market Order:    {'✅ PASS' if market_success else '❌ FAIL'}")
    print(f"Limit Order:     {'✅ PASS' if limit_success else '❌ FAIL'}")
    print(f"Log Files:       {'✅ PRESENT' if any(glob.glob('logs/*.log')) else '⚠️ MISSING'}")
    
    if client and market_success and limit_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your trading bot is working perfectly!")
        print("✅ You have both MARKET and LIMIT order logs")
        print("✅ Ready for submission!")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
    
    print("="*50)

if __name__ == "__main__":
    import glob
    main()
    
    # Pause so you can see results (useful when double-clicking)
    input("\nPress Enter to exit...")