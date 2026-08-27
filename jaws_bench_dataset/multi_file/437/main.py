# Main entry point for the penetration testing tool.

import argparse
from scanner import Scanner
from reporter import Reporter

def main():
    """
    Main function to parse arguments and initiate the penetration testing process.
    """
    parser = argparse.ArgumentParser(description="Penetration Testing Tool")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("--ports", nargs="+", type=int, help="List of ports to scan")
    parser.add_argument("--output", help="Output file for the report")

    args = parser.parse_args()

    # Initialize the scanner and reporter
    scanner = Scanner(args.target, args.ports)
    reporter = Reporter(args.output)

    # Perform the scan
    results = scanner.scan()

    # Generate the report
    reporter.generate_report(results)

if __name__ == "__main__":
    main()