"""Enhanced UI with rich formatting"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

console = Console()

def print_welcome():
    """Print welcome banner"""
    console.print(Panel.fit(
        "[bold cyan]🤖 Binance Futures Trading Bot[/bold cyan]\n"
        "[dim]Professional Trading Platform[/dim]",
        border_style="cyan"
    ))

def print_order_summary_enhanced(order: dict):
    """Print enhanced order summary"""
    table = Table(title="📋 Order Details", style="cyan")
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="white")
    
    fields = ['orderId', 'symbol', 'side', 'type', 'quantity', 'price', 'status', 'executedQty']
    for field in fields:
        value = order.get(field, 'N/A')
        if field == 'status' and value == 'FILLED':
            value = f"[green]{value}[/green]"
        elif field == 'status' and value == 'NEW':
            value = f"[yellow]{value}[/yellow]"
        table.add_row(field, str(value))
    
    console.print(table)
    
    if order.get('status') == 'FILLED':
        console.print("[green]✅ ORDER SUCCESSFULLY EXECUTED![/green]")
    else:
        console.print("[yellow]⏳ Order placed and waiting for execution[/yellow]")

def print_error(message: str):
    """Print error message"""
    console.print(f"[red]❌ ERROR: {message}[/red]")

def print_success(message: str):
    """Print success message"""
    console.print(f"[green]✅ {message}[/green]")