"""
DNS Enumeration Module
Fetches various DNS records for a given domain.
"""

import dns.resolver
import dns.exception
from colorama import Fore, Style

def enumerate_dns(domain):
    """
    Perform DNS enumeration on the target domain.
    
    Args:
        domain (str): The domain to query (e.g., 'example.com')
    
    Returns:
        dict: Dictionary containing all DNS records found
    """
    print(f"\n{Fore.CYAN}🔍 DNS Enumeration in progress...{Style.RESET_ALL}")
    
    results = {
        "A": [],
        "AAAA": [],
        "MX": [],
        "TXT": [],
        "NS": [],
        "CNAME": [],
        "SOA": None
    }
    
    # Record types to query
    record_types = ["A", "AAAA", "MX", "TXT", "NS", "CNAME"]
    
    for record_type in record_types:
        try:
            print(f"Querying {record_type} records...", end="")
            
            # Create a DNS resolver with custom settings
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5  # 5 second timeout
            resolver.lifetime = 5  # 5 second lifetime
            
            # Perform the query
            answers = resolver.resolve(domain, record_type)

              
            # Process the answers based on record type
            for answer in answers:
                if record_type == "MX":
                    # MX records have priority and exchange
                    mx_record = {
                        "priority": answer.preference,
                        "exchange": str(answer.exchange).rstrip('.')
                    }
                    results[record_type].append(mx_record)
                else:
                    # Simple record types (A, AAAA, TXT, NS, CNAME)
                    results[record_type].append(str(answer).rstrip('.'))
            
            print(f" {Fore.GREEN} Found {len(results[record_type])} records{Style.RESET_ALL}")