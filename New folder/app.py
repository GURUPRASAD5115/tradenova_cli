import streamlit as st
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Trading Bot",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("🚀 Binance Futures Trading Bot")
st.markdown("---")

# Initialize session state
if 'client' not in st.session_state:
    st.session_state['client'] = None
if 'connected' not in st.session_state:
    st.session_state['connected'] = False
if 'balance' not in st.session_state:
    st.session_state['balance'] = 0

# Function to connect to Binance
def connect_to_binance(api_key, api_secret):
    """Connect to Binance Futures Testnet"""
    try:
        client = Client(api_key, api_secret, testnet=True)
        # Test connection by fetching account
        account = client.futures_account()
        balance = float(account['totalWalletBalance'])
        return client, balance, None
    except BinanceAPIException as e:
        return None, 0, f"Binance API Error: {e.message}"
    except Exception as e:
        return None, 0, f"Connection Error: {str(e)}"

# Sidebar for API configuration
with st.sidebar:
    st.header("🔐 Binance Connection")
    
    # Try to load from .env first
    env_api_key = os.getenv('BINANCE_API_KEY', '')
    env_api_secret = os.getenv('BINANCE_API_SECRET', '')
    
    api_key = st.text_input(
        "API Key", 
        type="password", 
        value=env_api_key,
        key="api_key_input",
        help="Enter your Binance Testnet API Key"
    )
    
    api_secret = st.text_input(
        "API Secret", 
        type="password", 
        value=env_api_secret,
        key="api_secret_input",
        help="Enter your Binance Testnet API Secret"
    )
    
    st.markdown("---")
    st.caption("🔗 [Get API Keys from Binance Testnet](https://testnet.binancefuture.com/)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔌 Connect", key="connect_btn", use_container_width=True):
            if not api_key or not api_secret:
                st.error("❌ Please enter both API Key and Secret")
            else:
                with st.spinner("Connecting to Binance Futures Testnet..."):
                    client, balance, error = connect_to_binance(api_key, api_secret)
                    
                    if client:
                        st.session_state['client'] = client
                        st.session_state['connected'] = True
                        st.session_state['balance'] = balance
                        st.success(f"✅ Connected Successfully!")
                        st.info(f"💰 Balance: {balance:.2f} USDT")
                        st.rerun()
                    else:
                        st.error(f"❌ {error}")
    
    with col2:
        if st.button("🚪 Disconnect", key="disconnect_btn", use_container_width=True):
            st.session_state['client'] = None
            st.session_state['connected'] = False
            st.session_state['balance'] = 0
            st.success("✅ Disconnected")
            st.rerun()
    
    # Show connection status
    if st.session_state['connected']:
        st.markdown("---")
        st.success(f"🟢 Connected | Balance: {st.session_state['balance']:.2f} USDT")

# Main content area - only show if connected
if not st.session_state['connected']:
    st.info("👈 **Please connect to Binance using the sidebar**")
    st.markdown("""
    ### How to connect:
    1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com/)
    2. Register/Login
    3. Go to API Management
    4. Create new API key
    5. Copy API Key and Secret
    6. Paste them in the sidebar
    7. Click "Connect"
    
    ### Get Test Funds:
    - After connecting, claim free USDT from the faucet
    - You'll have 5000 USDT for testing
    """)
    
    # Show demo of what to expect
    with st.expander("📖 See Demo Preview"):
        st.image("https://testnet.binancefuture.com/static/images/logo.png", width=200)
        st.markdown("""
        **Once connected, you can:**
        - Place MARKET and LIMIT orders
        - View your balance
        - Check order status
        - See open orders
        """)
else:
    # User is connected - show trading interface
    st.success(f"🟢 Connected to Binance Futures Testnet | Balance: {st.session_state['balance']:.2f} USDT")
    
    # Create tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Place Order", "📋 Order Status", "💰 Account Balance", "📊 Open Orders"])
    
    # Tab 1: Place Order
    with tab1:
        st.subheader("📝 Place New Order")
        
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.text_input(
                "Symbol", 
                "BTCUSDT", 
                key="order_symbol",
                help="Example: BTCUSDT, ETHUSDT, BNBUSDT"
            ).upper()
            
            side = st.selectbox(
                "Side", 
                ["BUY", "SELL"], 
                key="order_side",
                help="BUY - Long position, SELL - Short position"
            )
            
            order_type = st.selectbox(
                "Order Type", 
                ["MARKET", "LIMIT"], 
                key="order_type",
                help="MARKET - Execute immediately at current price, LIMIT - Execute at specific price"
            )
            
            quantity = st.number_input(
                "Quantity", 
                min_value=0.001, 
                value=0.001, 
                step=0.001,
                key="order_quantity",
                help="Amount to trade (minimum depends on symbol)"
            )
            
            price = None
            if order_type == "LIMIT":
                price = st.number_input(
                    "Price (USDT)", 
                    min_value=0.01, 
                    value=25000.0, 
                    step=100.0,
                    key="order_price",
                    help="Limit price for the order"
                )
        
        with col2:
            st.subheader("📊 Order Preview")
            st.markdown(f"""
            | Field | Value |
            |-------|-------|
            | **Symbol** | {symbol} |
            | **Side** | {side} |
            | **Type** | {order_type} |
            | **Quantity** | {quantity} |
            {f"| **Price** | {price} |" if price else "| **Price** | Market Price |"}
            """)
            
            # Get current market price
            if st.session_state['client']:
                try:
                    ticker = st.session_state['client'].futures_symbol_ticker(symbol=symbol)
                    current_price = float(ticker['price'])
                    st.info(f"💰 Current {symbol} Price: ${current_price:,.2f}")
                    
                    if order_type == "LIMIT" and price:
                        if side == "BUY" and price > current_price:
                            st.warning(f"⚠️ Limit price {price} is above market price {current_price}")
                        elif side == "SELL" and price < current_price:
                            st.warning(f"⚠️ Limit price {price} is below market price {current_price}")
                        else:
                            st.success("✅ Order price is reasonable")
                except Exception as e:
                    st.warning(f"Could not fetch current price: {e}")
        
        # Place Order Button
        if st.button("🚀 PLACE ORDER", type="primary", key="place_order_btn", use_container_width=True):
            if st.session_state['client'] is None:
                st.error("❌ Not connected to Binance!")
            else:
                try:
                    with st.spinner("Placing order on Binance..."):
                        if order_type == "MARKET":
                            order = st.session_state['client'].futures_create_order(
                                symbol=symbol,
                                side=side,
                                type=order_type,
                                quantity=quantity
                            )
                        else:
                            order = st.session_state['client'].futures_create_order(
                                symbol=symbol,
                                side=side,
                                type=order_type,
                                quantity=quantity,
                                price=price,
                                timeInForce='GTC'
                            )
                        
                        st.success("✅ ORDER PLACED SUCCESSFULLY!")
                        
                        # Display order details
                        st.json({
                            "Order ID": order['orderId'],
                            "Symbol": order['symbol'],
                            "Side": order['side'],
                            "Type": order['type'],
                            "Quantity": order['origQty'],
                            "Price": order.get('price', 'Market'),
                            "Status": order['status'],
                            "Executed Qty": order['executedQty']
                        })
                        
                except BinanceAPIException as e:
                    st.error(f"❌ Binance Error: {e.message}")
                except Exception as e:
                    st.error(f"❌ Order Failed: {str(e)}")
    
    # Tab 2: Order Status
    with tab2:
        st.subheader("🔍 Check Order Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            order_id = st.text_input("Order ID", key="status_order_id")
            symbol_status = st.text_input("Symbol", "BTCUSDT", key="status_symbol").upper()
        
        with col2:
            if st.button("🔍 Check Order", key="check_order_btn", use_container_width=True):
                if not order_id:
                    st.error("Please enter Order ID")
                else:
                    try:
                        order = st.session_state['client'].futures_get_order(
                            symbol=symbol_status,
                            orderId=int(order_id)
                        )
                        
                        st.success("✅ Order Found!")
                        
                        # Display in nice format
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Order ID", order['orderId'])
                            st.metric("Symbol", order['symbol'])
                            st.metric("Side", order['side'])
                            st.metric("Type", order['type'])
                        with col_b:
                            st.metric("Status", order['status'])
                            st.metric("Quantity", order['origQty'])
                            st.metric("Executed", order['executedQty'])
                            st.metric("Price", order.get('price', 'Market'))
                        
                    except BinanceAPIException as e:
                        st.error(f"❌ Error: {e.message}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Tab 3: Account Balance
    with tab3:
        st.subheader("💰 Account Information")
        
        if st.button("🔄 Refresh Balance", key="refresh_balance_btn", use_container_width=True):
            with st.spinner("Fetching latest balance..."):
                try:
                    account = st.session_state['client'].futures_account()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "💰 Total Balance", 
                            f"{float(account['totalWalletBalance']):.2f} USDT",
                            delta=None
                        )
                    with col2:
                        st.metric(
                            "📊 Available Balance", 
                            f"{float(account['availableBalance']):.2f} USDT"
                        )
                    with col3:
                        st.metric(
                            "📈 Unrealized PnL", 
                            f"{float(account['totalUnrealizedProfit']):.2f} USDT"
                        )
                    
                    # Show all assets with balance
                    assets = []
                    for asset in account['assets']:
                        if float(asset['walletBalance']) > 0:
                            assets.append({
                                'Asset': asset['asset'],
                                'Wallet Balance': f"{float(asset['walletBalance']):.4f}",
                                'Available': f"{float(asset['availableBalance']):.4f}",
                                'Cross Wallet': f"{float(asset['crossWalletBalance']):.4f}"
                            })
                    
                    if assets:
                        st.subheader("📦 All Asset Balances")
                        st.dataframe(pd.DataFrame(assets), use_container_width=True)
                    else:
                        st.info("No assets with balance")
                        
                except Exception as e:
                    st.error(f"❌ Failed to fetch balance: {str(e)}")
    
    # Tab 4: Open Orders
    with tab4:
        st.subheader("📋 Open Orders")
        
        symbol_filter = st.text_input("Filter by Symbol (optional, leave empty for all)", key="filter_symbol").upper()
        
        if st.button("📋 View Open Orders", key="view_orders_btn", use_container_width=True):
            with st.spinner("Fetching open orders..."):
                try:
                    if symbol_filter:
                        orders = st.session_state['client'].futures_get_open_orders(symbol=symbol_filter)
                    else:
                        orders = st.session_state['client'].futures_get_open_orders()
                    
                    if not orders:
                        st.info("No open orders found")
                    else:
                        orders_data = []
                        for order in orders:
                            orders_data.append({
                                'Order ID': order['orderId'],
                                'Symbol': order['symbol'],
                                'Side': order['side'],
                                'Type': order['type'],
                                'Quantity': order['origQty'],
                                'Price': order.get('price', 'Market'),
                                'Status': order['status'],
                                'Time': datetime.fromtimestamp(order['time']/1000).strftime('%Y-%m-%d %H:%M:%S')
                            })
                        
                        st.dataframe(pd.DataFrame(orders_data), use_container_width=True)
                        
                        # Cancel order option
                        st.subheader("❌ Cancel Order")
                        cancel_id = st.text_input("Enter Order ID to cancel", key="cancel_order_id")
                        if st.button("Cancel Order", key="cancel_btn"):
                            try:
                                result = st.session_state['client'].futures_cancel_order(
                                    symbol=symbol_filter if symbol_filter else "BTCUSDT",
                                    orderId=int(cancel_id)
                                )
                                st.success(f"✅ Order {cancel_id} cancelled successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Failed to cancel: {str(e)}")
                        
                except Exception as e:
                    st.error(f"❌ Failed to fetch orders: {str(e)}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col2:
    st.caption("🔗 Binance Futures Testnet")
with col3:
    st.caption("🤖 Trading Bot v1.0")