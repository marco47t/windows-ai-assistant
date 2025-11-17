"""CLI interface for Windows AI Assistant."""

import os
import sys
import re
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from colorama import init, Fore, Style

from core.config import settings
from core.database import init_db
from services.chat_service import ChatService
from services.router import AIRouter
from tools.tool_manager import ToolManager  # NEW

# Initialize colorama
init()

console = Console()


def print_banner():
    """Print welcome banner."""
    banner = """
    ╔══════════════════════════════════════════╗
    ║   🤖 Windows AI Assistant CLI v1.0      ║
    ║   Powered by Groq + Gemini              ║
    ║   🔍 Web Search & Navigation Enabled    ║
    ╚══════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def print_help():
    """Print available commands."""
    help_text = """
    **Available Commands:**
    
    - `!groq` - Force use Groq AI
    - `!gemini` - Force use Gemini AI
    - `!auto` - Auto-select AI provider (default)
    - `!search <query>` - Search the web
    - `!read <url>` - Read a webpage
    - `!history` - Show conversation history
    - `!clear` - Clear current conversation
    - `!help` - Show this help message
    - `!exit` or `!quit` - Exit the program
    
    **Just type your message to chat!**
    **The AI can automatically search the web when needed.**
    """
    console.print(Panel(Markdown(help_text), title="Help", border_style="green"))


def detect_web_search_intent(message: str) -> bool:
    """Detect if user wants to search the web.
    
    Args:
        message: User message
        
    Returns:
        True if web search is needed
    """
    search_keywords = [
        'search for', 'google', 'find information about',
        'look up', 'what is the latest', 'current news',
        'search the web', 'search', 'find'
    ]
    
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in search_keywords)


def main():
    """Main CLI loop."""
    # Initialize database
    init_db()
    
    # Initialize services
    router = AIRouter()
    chat_service = ChatService(router)
    tool_manager = ToolManager()  # NEW
    
    # Print banner
    print_banner()
    print_help()
    
    console.print("\n[bold green]Ready![/bold green] Start chatting or type !help for commands.\n")
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = console.input("[bold blue]You:[/bold blue] ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("!"):
                command = user_input.lower()
                
                if command in ["!exit", "!quit"]:
                    console.print("\n[bold yellow]Goodbye! 👋[/bold yellow]\n")
                    break
                    
                elif command == "!help":
                    print_help()
                    continue
                    
                elif command == "!groq":
                    router.set_provider("groq")
                    console.print("[green]✓ Switched to Groq AI[/green]\n")
                    continue
                    
                elif command == "!gemini":
                    router.set_provider("gemini")
                    console.print("[green]✓ Switched to Gemini AI[/green]\n")
                    continue
                    
                elif command == "!auto":
                    router.set_provider("auto")
                    console.print("[green]✓ Auto-routing enabled[/green]\n")
                    continue
                    
                elif command == "!clear":
                    chat_service.clear_history()
                    console.print("[green]✓ Conversation cleared[/green]\n")
                    continue
                    
                elif command == "!history":
                    history = chat_service.get_history()
                    if history:
                        console.print("\n[bold]Conversation History:[/bold]\n")
                        for msg in history:
                            role = "You" if msg['role'] == 'user' else 'AI'
                            color = "blue" if msg['role'] == 'user' else 'green'
                            console.print(f"[{color}]{role}:[/{color}] {msg['content']}\n")
                    else:
                        console.print("[yellow]No conversation history yet.[/yellow]\n")
                    continue
                
                # NEW: Web search command
                elif command.startswith("!search "):
                    query = user_input[8:].strip()
                    with console.status("[bold green]Searching...", spinner="dots"):
                        result = tool_manager.web_search(query)
                    console.print("\n[bold green]Search Results:[/bold green]")
                    console.print(Panel(Markdown(result), border_style="green"))
                    console.print()
                    continue
                
                # NEW: Read webpage command
                elif command.startswith("!read "):
                    url = user_input[6:].strip()
                    with console.status("[bold green]Reading webpage...", spinner="dots"):
                        result = tool_manager.read_webpage(url)
                    console.print("\n[bold green]Webpage Content:[/bold green]")
                    console.print(Panel(Markdown(result), border_style="green"))
                    console.print()
                    continue

                elif command.startswith("!open "):
                    app = user_input[6:].strip()
                    result = tool_manager.open_app(app)
                    console.print(f"[green]{result}[/green]\n")
                    continue

                elif command.startswith("!code "):
                    code = user_input[6:].strip()
                    with console.status("[bold green]Executing code...", spinner="dots"):
                        result = tool_manager.execute_code(code)
                    console.print(Panel(Markdown(result), border_style="green"))
                    continue

                elif command.startswith("!calc "):
                    expr = user_input[6:].strip()
                    result = tool_manager.calculate(expr)
                    console.print(f"[green]{result}[/green]\n")
                    continue

                elif command == "!screenshot":
                    result = tool_manager.take_screenshot()
                    console.print(f"[green]{result}[/green]\n")
                    continue

                elif command.startswith("!agent "):
                    task = user_input[7:].strip()
                    with console.status("[bold green]Multi-agent processing...", spinner="dots"):
                        from services.agent_system import agent_system
                        if agent_system:
                            results = agent_system.execute_task(task)
                            console.print(Panel(Markdown(results['final']), border_style="green"))
                    continue
                    
                else:
                    console.print(f"[red]Unknown command: {command}[/red]\n")
                    continue
            
            # Check if we should auto-search
            should_search = detect_web_search_intent(user_input)
            
            if should_search:
                # Extract search query (simple extraction)
                query_match = re.search(r'(?:search|find|look up|google)\s+(?:for\s+)?(.+)', user_input, re.IGNORECASE)
                if query_match:
                    query = query_match.group(1).strip()
                    
                    with console.status("[bold green]Searching web...", spinner="dots"):
                        search_results = tool_manager.web_search(query, max_results=3)
                    
                    # Add search results to context
                    enhanced_prompt = f"{user_input}\n\nWeb Search Results:\n{search_results}"
                    user_input = enhanced_prompt
            
            # Send message and get response
            with console.status("[bold green]AI is thinking...", spinner="dots"):
                response, provider = chat_service.send_message(user_input)
            
            # Display response
            provider_badge = f"[{provider.upper()}]"
            console.print(f"\n[bold green]AI {provider_badge}:[/bold green]")
            console.print(Panel(Markdown(response), border_style="green"))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Interrupted. Type !exit to quit.[/bold yellow]\n")
            continue
            
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}\n")
            continue


if __name__ == "__main__":
    main()
