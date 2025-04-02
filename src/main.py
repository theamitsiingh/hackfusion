#!/usr/bin/env python3
"""
Main entry point for HackFusion
"""

import os
import sys
from rich.console import Console

# Add src directory to Python path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from src.menu import Menu

def main():
    """Main entry point"""
    try:
        console = Console()
        menu = Menu()
        menu.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
