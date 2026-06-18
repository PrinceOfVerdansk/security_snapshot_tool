
"""
Security Snapshot Tool - Main Entry Point
A lightweight security assessment tool for domain reconnaissance.
"""

import sys
import argparse
from datetime import datetime
from colorama import init, Fore, Style

# Import your modules (we'll build these next)
from src.dns_enum import enumerate_dns
from src.header_check import check_headers
from src.subdomain_brute import brute_subdomains
from src.ssl_check import check_ssl
from src.report_generator import generate_report

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_banner():
    """Display the tool banner."""
    banner = f"""
{Fore.CYAN}{'='*60}
{Fore.GREEN}   SECURITY SNAPSHOT TOOL v1.0
{Fore.YELLOW}   Lightweight Security Assessment
{Fore.CYAN}{'='*60}
{Fore.WHITE}   Target: Domain Reconnaissance
   Author: [Your Name]
   Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
{Fore.CYAN}{'='*60}
"""
    print(banner)

