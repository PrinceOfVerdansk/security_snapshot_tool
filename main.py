
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
{Fore.GREEN}   🔒 SECURITY SNAPSHOT TOOL v1.0
{Fore.YELLOW}   Lightweight Security Assessment
{Fore.CYAN}{'='*60}
{Fore.WHITE}   Target: Domain Reconnaissance
   Author: [Your Name]
   Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
{Fore.CYAN}{'='*60}
"""
    print(banner)

def main():
    """Main program entry point."""
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Security Snapshot Tool - Perform security reconnaissance on a domain"
    )
    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Target domain to analyze (e.g., example.com)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output filename for the report (default: report.html)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    print(f"{Fore.YELLOW}🎯 Target Domain: {Fore.WHITE}{args.domain}")
    print(f"{Fore.YELLOW}📋 Starting scan...{Style.RESET_ALL}\n")
    
    # Initialize results dictionary
    results = {
        "domain": args.domain,
        "scan_time": datetime.now().isoformat(),
        "dns": {},
        "headers": {},
        "subdomains": [],
        "ssl": {},
        "vulnerabilities": []
    }
    
    # TODO: Call each module here
    # We'll implement these in the coming days
    
    print(f"\n{Fore.GREEN}✅ Scan completed!")
    print(f"{Fore.YELLOW}📄 Generating report...")
    
    # Generate report
    output_file = args.output or f"reports/{args.domain}_report.html"
    generate_report(results, output_file)
    
    print(f"{Fore.GREEN}✅ Report saved to: {Fore.WHITE}{output_file}")
    print(f"\n{Fore.CYAN}💡 Open the HTML file in your browser to view results")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ An unexpected error occurred: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)