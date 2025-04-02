"""
Menu system for HackFusion
"""

import sys
import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich import box

from src.utils.config_loader import ConfigLoader
from src.tools_integration.information_gathering import InformationGathering
from src.tools_integration.vulnerability_analysis import VulnerabilityAnalysis
from src.tools_integration.web_application import WebApplicationAnalysis
from src.tools_integration.wireless_attacks import WirelessAttacks
from src.ai_assistant import AIAssistant

class Menu:
    """Main menu class"""
    
    def __init__(self):
        """Initialize menu"""
        self.console = Console()
        
        # Initialize AI assistant if API key is available
        try:
            self.ai_assistant = AIAssistant()
            self.has_ai = True
        except Exception as e:
            self.console.print(f"[red]AI Assistant not available: {e}[/red]")
            self.console.print("[yellow]To enable AI features, set the OPENAI_API_KEY environment variable[/yellow]")
            self.has_ai = False
            
        # Initialize tool modules
        self.init_modules()
        
    def init_modules(self):
        """Initialize tool modules"""
        try:
            self.info_gathering = InformationGathering()
            self.vuln_analysis = VulnerabilityAnalysis()
            self.web_analysis = WebApplicationAnalysis()
            self.wireless = WirelessAttacks()
        except Exception as e:
            self.console.print(f"[red]Error initializing modules: {e}[/red]")
            sys.exit(1)
            
    def print_menu(self):
        """Print main menu"""
        table = Table(title="HackFusion Menu", box=box.ROUNDED)
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="green")
        
        table.add_row("1", "AI Assistant (Natural Language Interface)")
        table.add_row("2", "Information Gathering")
        table.add_row("3", "Vulnerability Analysis")
        table.add_row("4", "Web Application Analysis")
        table.add_row("5", "Wireless Network Analysis")
        table.add_row("q", "Quit")
        
        self.console.print(table)
        
    def run(self):
        """Run main menu loop"""
        while True:
            self.console.clear()
            self.print_menu()
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "q"])
            
            if choice == "q":
                self.console.print("[yellow]Goodbye![/yellow]")
                sys.exit(0)
                
            try:
                if choice == "1" and self.has_ai:
                    self.ai_menu()
                elif choice == "2":
                    self.info_gathering_menu()
                elif choice == "3":
                    self.vuln_analysis_menu()
                elif choice == "4":
                    self.web_analysis_menu()
                elif choice == "5":
                    self.wireless_menu()
                else:
                    self.console.print("[red]Invalid choice or AI not available[/red]")
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
                
    def ai_menu(self):
        """AI-assisted menu"""
        self.console.print(Panel.fit(
            "[green]AI Assistant[/green]\n\n"
            "Describe what you want to do in natural language.\n"
            "Examples:\n"
            "- Scan a network for vulnerabilities\n"
            "- Test a web application for SQL injection\n"
            "- Check wireless networks for security issues"
        ))
        
        request = Prompt.ask("What would you like to do")
        
        try:
            plan = self.ai_assistant.analyze_request(request)
            self.execute_ai_plan(plan)
        except Exception as e:
            self.console.print(f"[red]AI Error: {str(e)}[/red]")
            
    def execute_ai_plan(self, plan: Dict[str, Any]):
        """Execute AI-generated action plan"""
        self.console.print(Panel(f"[blue]Category:[/blue] {plan['category']}\n"
                               f"[blue]Description:[/blue] {plan['description']}\n"
                               f"[blue]Tools:[/blue] {', '.join(plan['tools'])}"))
                               
        for step in plan['steps']:
            self.console.print(f"\n[yellow]Step:[/yellow] {step['action']}")
            self.console.print(f"[blue]Tool:[/blue] {step['tool']}")
            self.console.print(f"[blue]Description:[/blue] {step['description']}")
            
            # Execute step based on tool category
            if step['tool'] == 'nmap':
                result = self.info_gathering.run_nmap_scan(**step['params'])
            elif step['tool'] == 'sqlmap':
                result = self.web_analysis.run_scan(**step['params'])
            elif step['tool'] == 'airmon-ng':
                result = self.wireless.run_scan(**step['params'])
            else:
                self.console.print(f"[red]Unknown tool: {step['tool']}[/red]")
                continue
                
            # Print results
            if isinstance(result, dict):
                for key, value in result.items():
                    self.console.print(f"[green]{key}:[/green] {value}")
            else:
                self.console.print(str(result))
                
    def info_gathering_menu(self):
        """Information gathering menu"""
        target = Prompt.ask("Enter target (IP, domain, or network range)")
        
        table = Table(title="Information Gathering Results", box=box.ROUNDED)
        table.add_column("Tool", style="cyan")
        table.add_column("Results", style="green")
        
        # Run various info gathering tools
        try:
            nmap_result = self.info_gathering.run_nmap_scan(target)
            whois_result = self.info_gathering.run_whois_lookup(target)
            dns_result = self.info_gathering.run_dns_enum(target)
            
            table.add_row("Nmap", str(nmap_result))
            table.add_row("WHOIS", str(whois_result))
            table.add_row("DNS", str(dns_result))
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
            
    def vuln_analysis_menu(self):
        """Vulnerability analysis menu"""
        target = Prompt.ask("Enter target (IP or domain)")
        
        try:
            results = self.vuln_analysis.run_scan(target)
            
            table = Table(title="Vulnerability Analysis Results", box=box.ROUNDED)
            table.add_column("Category", style="cyan")
            table.add_column("Details", style="green")
            
            for category, details in results.items():
                table.add_row(category, str(details))
                
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
            
    def web_analysis_menu(self):
        """Web application analysis menu"""
        target = Prompt.ask("Enter target URL")
        
        try:
            results = self.web_analysis.run_scan(target)
            
            table = Table(title="Web Application Analysis Results", box=box.ROUNDED)
            table.add_column("Tool", style="cyan")
            table.add_column("Results", style="green")
            
            for tool, result in results.items():
                if isinstance(result, dict) and 'error' in result:
                    table.add_row(tool, f"[red]{result['error']}[/red]")
                else:
                    table.add_row(tool, str(result))
                    
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
            
    def wireless_menu(self):
        """Wireless network analysis menu"""
        interface = Prompt.ask("Enter wireless interface (e.g., wlan0)")
        
        try:
            results = self.wireless.run_scan(interface)
            
            table = Table(title="Wireless Network Analysis Results", box=box.ROUNDED)
            table.add_column("Network", style="cyan")
            table.add_column("Details", style="green")
            
            for network, details in results.items():
                table.add_row(network, str(details))
                
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
