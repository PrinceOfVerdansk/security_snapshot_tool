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
            
        except dns.resolver.NoAnswer:
            print(f" {Fore.YELLOW}⚠️  No {record_type} records found{Style.RESET_ALL}")
            results[record_type] = []
            
        except dns.resolver.NXDOMAIN:
            print(f" {Fore.RED} Domain does not exist{Style.RESET_ALL}")
            return None
            
        except dns.resolver.Timeout:
            print(f" {Fore.RED} Timeout while querying {record_type}{Style.RESET_ALL}")
            results[record_type] = []
            
        except dns.exception.DNSException as e:
            print(f" {Fore.RED} DNS Error: {str(e)}{Style.RESET_ALL}")
            results[record_type] = []
    
    # Get SOA record separately (special handling)
    try:
        print("   Querying SOA records...", end="")
        soa_answer = dns.resolver.resolve(domain, "SOA")
        if soa_answer:
            soa = soa_answer[0]
            results["SOA"] = {
                "mname": str(soa.mname).rstrip('.'),
                "rname": str(soa.rname).rstrip('.'),
                "serial": soa.serial,
                "refresh": soa.refresh,
                "retry": soa.retry,
                "expire": soa.expire,
                "minimum": soa.minimum
            }
            print(f" {Fore.GREEN} SOA record found{Style.RESET_ALL}")
    except Exception as e:
        print(f" {Fore.YELLOW}  No SOA record found: {str(e)}{Style.RESET_ALL}")
        results["SOA"] = None
    
    return results

def display_dns_results(results):
    """Pretty print DNS results to the console."""
    if not results:
        return
    
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.GREEN}📊 DNS ENUMERATION RESULTS")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # A Records
    if results.get("A"):
        print(f"\n{Fore.YELLOW} A Records (IPv4):{Style.RESET_ALL}")
        for ip in results["A"]:
            print(f"  → {ip}")
    
    # AAAA Records
    if results.get("AAAA"):
        print(f"\n{Fore.YELLOW} AAAA Records (IPv6):{Style.RESET_ALL}")
        for ip in results["AAAA"]:
            print(f"  → {ip}")
    
    # MX Records
    if results.get("MX"):
        print(f"\n{Fore.YELLOW}📧 MX Records (Mail Exchangers):{Style.RESET_ALL}")
        for mx in results["MX"]:
            print(f"  → Priority {mx['priority']}: {mx['exchange']}")
    
    # TXT Records
    if results.get("TXT"):
        print(f"\n{Fore.YELLOW}📝 TXT Records:{Style.RESET_ALL}")
        for txt in results["TXT"]:
            # Truncate long TXT records for display
            display_txt = txt[:100] + "..." if len(txt) > 100 else txt
            print(f"  → {display_txt}")
    
    # NS Records
    if results.get("NS"):
        print(f"\n{Fore.YELLOW}🌐 NS Records (Name Servers):{Style.RESET_ALL}")
        for ns in results["NS"]:
            print(f"  → {ns}")
    
    # CNAME Records
    if results.get("CNAME"):
        print(f"\n{Fore.YELLOW}🔗 CNAME Records (Aliases):{Style.RESET_ALL}")
        for cname in results["CNAME"]:
            print(f"  → {cname}")
    
    # SOA Record
    if results.get("SOA"):
        soa = results["SOA"]
        print(f"\n{Fore.YELLOW}📋 SOA Record (Start of Authority):{Style.RESET_ALL}")
        print(f"  → Primary NS: {soa['mname']}")
        print(f"  → Responsible Email: {soa['rname']}")
        print(f"  → Serial: {soa['serial']}")
        print(f"  → Refresh: {soa['refresh']}s")
        print(f"  → Retry: {soa['retry']}s")
        print(f"  → Expire: {soa['expire']}s")
        print(f"  → Minimum TTL: {soa['minimum']}s")

if __name__ == "__main__":
    # Test the module
    test_domain = "example.com"
    print(f"Testing DNS enumeration on {test_domain}...")
    results = enumerate_dns(test_domain)
    if results:
        display_dns_results(results)