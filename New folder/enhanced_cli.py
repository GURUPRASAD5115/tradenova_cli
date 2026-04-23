#!/usr/bin/env python3
"""
Enhanced CLI for Trading Bot - Bonus Features
Includes: Rich UI, Menus, Stop-Limit Orders, Balance Display
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional

# Rich library for beautiful UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich library not installed. Install with: pip install rich")

# Import bot modules
from bot.logging_config import setup_logging, get_logger
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_quantity, validate_price

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

# Initialize Rich console if available
if RICH_AVAILABLE:
    console = Console()
else:
    console = None

class EnhancedTradingBot:
    """Enhanced trading bot with menu system and rich UI"""
    
    def __init__(self):
        """Initialize the enhanced bot"""
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.client = None
        self.order_manager = None
        
    def initialize(self):
        """Initialize connection to Binance"""
        if not self.api_key or not self.api_secret:
            self.print_error("API credentials not found! Set BINANCE_API_KEY and BINANCE_API_SECRET")
            return False
        
        try:
            if console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description="Connecting to Binance...", total=None)
                    self.client = BinanceFuturesClient(self.api_key, self.api_secret, testnet=True)
            else:
                self.client = BinanceFuturesClient(self.api_key, self.api_secret, testnet=True)
            
            self.order_manager = OrderManager(self.client)
            
            # Get account info
            account_info = self.client.get_account_info()
            balance = float(account_info['totalWalletBalance'])
            
            self.print_success(f"Connected! Balance: {balance:.2f} USDT")
            return True
            
        except Exception as e:
            self.print_error(f"Connection failed: {e}")
            return False
    
    def print_welcome(self):
        """Print welcome banner"""
        if console:
            console.clear()
            welcome_text = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
║  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
║  ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌
║  ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
║  ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
║  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
║   ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
║            ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌
║   ▄▄▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌
║  ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
║   ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
║                                                              ║
║         BINANCE FUTURES TRADING BOT - ENHANCED EDITION       ║
╚══════════════════════════════════════════════════════════════╝
            """
            console.print(Panel(welcome_text, border_style="cyan"))
        else:
            print("\n" + "="*60)
            print("🚀 BINANCE FUTURES TRADING BOT - ENHANCED EDITION")
            print("="*60)
    
    def print_success(self, message: str):
        """Print success message"""
        if console:
            console.print(f"[green]✅ {message}[/green]")
        else:
            print(f"✅ {message}")
    
    def print_error(self, message: str):
        """Print error message"""
        if console:
            console.print(f"[red]❌ {message}[/red]")
        else:
            print(f"❌ {message}")
    
    def print_info(self, message: str):
        """Print info message"""
        if console:
            console.print(f"[cyan]ℹ️  {message}[/cyan]")
        else:
            print(f"ℹ️ {message}")
    
    def show_balance(self):
        """Display account balance"""
        try:
            account_info = self.client.get_account_info()
            
            if console:
                table = Table(title="📊 Account Balance", style="cyan")
                table.add_column("Asset", style="bold cyan")
                table.add_column("Wallet Balance", style="green")
                table.add_column("Available Balance", style="yellow")
                
                for asset in account_info.get('assets', []):
                    if float(asset['walletBalance']) > 0:
                        table.add_row(
                            asset['asset'],
                            f"{float(asset['walletBalance']):.2f}",
                            f"{float(asset['availableBalance']):.2f}"
                        )
                
                table.add_row("TOTAL", f"{float(account_info['totalWalletBalance']):.2f}", "")
                console.print(table)
            else:
                print(f"Total Balance: {account_info['totalWalletBalance']} USDT")
            
        except Exception as e:
            self.print_error(f"Failed to get balance: {e}")
    
    def show_open_orders(self, symbol: str = None):
        """Display open orders"""
        try:
            if symbol:
                orders = self.client.client.futures_get_open_orders(symbol=symbol)
            else:
                orders = self.client.client.futures_get_open_orders()
            
            if not orders:
                self.print_info("No open orders")
                return
            
            if console:
                table = Table(title="📋 Open Orders", style="cyan")
                table.add_column("Order ID", style="yellow")
                table.add_column("Symbol", style="cyan")
                table.add_column("Side", style="white")
                table.add_column("Type", style="white")
                table.add_column("Quantity", style="green")
                table.add_column("Price", style="yellow")
                table.add_column("Status", style="magenta")
                
                for order in orders:
                    table.add_row(
                        str(order['orderId']),
                        order['symbol'],
                        order['side'],
                        order['type'],
                        order['origQty'],
                        order.get('price', '0'),
                        order['status']
                    )
                
                console.print(table)
            else:
                for order in orders:
                    print(f"Order {order['orderId']}: {order['symbol']} {order['side']} {order['type']}")
            
        except Exception as e:
            self.print_error(f"Failed to get orders: {e}")
    
    def place_order_menu(self):
        """Interactive menu for placing orders"""
        if console:
            console.clear()
            console.print(Panel("[bold cyan]📝 Place New Order[/bold cyan]", border_style="cyan"))
        else:
            print("\n📝 Place New Order")
            print("-" * 40)
        
        # Get symbol
        while True:
            symbol = Prompt.ask("Symbol", default="BTCUSDT").upper()
            is_valid, msg = validate_symbol(symbol)
            if is_valid:
                break
            self.print_error(msg)
        
        # Get side
        side = Prompt.ask("Side", choices=["BUY", "SELL"])
        
        # Get order type
        order_type = Prompt.ask(
            "Order Type", 
            choices=["MARKET", "LIMIT", "STOP_LIMIT"]
        )
        
        # Get quantity
        while True:
            try:
                quantity = float(Prompt.ask("Quantity", default="0.001"))
                is_valid, msg = validate_quantity(quantity)
                if is_valid:
                    break
                self.print_error(msg)
            except ValueError:
                self.print_error("Invalid quantity")
        
        # Get price for limit orders
        price = None
        if order_type in ["LIMIT", "STOP_LIMIT"]:
            while True:
                try:
                    price = float(Prompt.ask("Limit Price"))
                    is_valid, msg = validate_price(price, order_type)
                    if is_valid:
                        break
                    self.print_error(msg)
                except ValueError:
                    self.print_error("Invalid price")
        
        # Get stop price for stop-limit orders
        stop_price = None
        if order_type == "STOP_LIMIT":
            while True:
                try:
                    stop_price = float(Prompt.ask("Stop Price"))
                    break
                except ValueError:
                    self.print_error("Invalid stop price")
        
        # Display summary
        if console:
            summary_table = Table(title="📝 Order Summary", style="cyan")
            summary_table.add_column("Field", style="bold cyan")
            summary_table.add_column("Value", style="white")
            summary_table.add_row("Symbol", symbol)
            summary_table.add_row("Side", side)
            summary_table.add_row("Type", order_type)
            summary_table.add_row("Quantity", str(quantity))
            if price:
                summary_table.add_row("Limit Price", str(price))
            if stop_price:
                summary_table.add_row("Stop Price", str(stop_price))
            console.print(summary_table)
        else:
            print(f"\nOrder Summary:")
            print(f"  Symbol: {symbol}")
            print(f"  Side: {side}")
            print(f"  Type: {order_type}")
            print(f"  Quantity: {quantity}")
            if price:
                print(f"  Price: {price}")
        
        # Confirm
        if not Confirm.ask("\nConfirm order?"):
            self.print_info("Order cancelled")
            return
        
        # Place order
        try:
            if order_type == "STOP_LIMIT":
                # Place stop-limit order
                order = self.client.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='STOP',
                    quantity=quantity,
                    stopPrice=stop_price,
                    price=price,
                    timeInForce='GTC'
                )
            else:
                order = self.order_manager.place_order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    price=price
                )
            
            # Display result
            if console:
                result_table = Table(title="✅ Order Result", style="green")
                result_table.add_column("Field", style="bold green")
                result_table.add_column("Value", style="white")
                result_table.add_row("Order ID", str(order.get('orderId', 'N/A')))
                result_table.add_row("Status", order.get('status', 'N/A'))
                result_table.add_row("Executed Qty", order.get('executedQty', '0'))
                result_table.add_row("Avg Price", str(order.get('avgPrice', 'N/A')))
                console.print(result_table)
            else:
                print(f"\n✅ ORDER SUCCESSFUL!")
                print(f"  Order ID: {order.get('orderId')}")
                print(f"  Status: {order.get('status')}")
            
            self.print_success("Order placed successfully!")
            
        except Exception as e:
            self.print_error(f"Order failed: {e}")
        
        if console:
            Prompt.ask("\nPress Enter to continue")
    
    def cancel_order_menu(self):
        """Menu to cancel orders"""
        self.show_open_orders()
        
        if not Confirm.ask("\nCancel an order?"):
            return
        
        order_id = int(Prompt.ask("Enter Order ID to cancel"))
        symbol = Prompt.ask("Symbol", default="BTCUSDT").upper()
        
        try:
            result = self.client.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            self.print_success(f"Order {order_id} cancelled")
        except Exception as e:
            self.print_error(f"Failed to cancel order: {e}")
    
    def main_menu(self):
        """Main interactive menu"""
        while True:
            if console:
                console.clear()
                self.print_welcome()
                
                menu_table = Table(title="📊 Main Menu", style="cyan")
                menu_table.add_column("Option", style="bold yellow")
                menu_table.add_column("Action", style="white")
                menu_table.add_row("1", "💰 Place Order")
                menu_table.add_row("2", "📋 View Open Orders")
                menu_table.add_row("3", "💵 View Balance")
                menu_table.add_row("4", "❌ Cancel Order")
                menu_table.add_row("5", "ℹ️  Account Info")
                menu_table.add_row("6", "🚪 Exit")
                console.print(menu_table)
                
                choice = Prompt.ask("\n[bold cyan]Select option[/bold cyan]", 
                                   choices=["1", "2", "3", "4", "5", "6"])
            else:
                print("\n" + "="*40)
                print("MAIN MENU")
                print("="*40)
                print("1. Place Order")
                print("2. View Open Orders")
                print("3. View Balance")
                print("4. Cancel Order")
                print("5. Account Info")
                print("6. Exit")
                choice = input("\nSelect option: ")
            
            if choice == "1":
                self.place_order_menu()
            elif choice == "2":
                symbol = Prompt.ask("Symbol (optional)", default="") if console else input("Symbol (optional): ")
                self.show_open_orders(symbol if symbol else None)
                if console:
                    Prompt.ask("\nPress Enter to continue")
            elif choice == "3":
                self.show_balance()
                if console:
                    Prompt.ask("\nPress Enter to continue")
            elif choice == "4":
                self.cancel_order_menu()
                if console:
                    Prompt.ask("\nPress Enter to continue")
            elif choice == "5":
                account_info = self.client.get_account_info()
                if console:
                    table = Table(title="Account Info")
                    table.add_column("Field", style="cyan")
                    table.add_column("Value", style="white")
                    table.add_row("Can Trade", str(account_info.get('canTrade', 'N/A')))
                    table.add_row("Can Withdraw", str(account_info.get('canWithdraw', 'N/A')))
                    table.add_row("Fee Tier", str(account_info.get('feeTier', 'N/A')))
                    console.print(table)
                else:
                    print(f"Account Info: {account_info}")
                if console:
                    Prompt.ask("\nPress Enter to continue")
            elif choice == "6":
                self.print_success("Goodbye! 👋")
                sys.exit(0)
    
    def run(self):
        """Run the enhanced bot"""
        if not self.initialize():
            return
        
        try:
            self.main_menu()
        except KeyboardInterrupt:
            self.print_info("\nBot stopped by user")
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")
            logger.critical(f"Fatal error: {e}", exc_info=True)

def main():
    """Main entry point"""
    bot = EnhancedTradingBot()
    bot.run()

if __name__ == "__main__":
    main()