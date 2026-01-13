"""
Main application script for Mortgage Statement Parser

Usage:
    python app.py <path_to_mortgage_statement>
    python app.py --url <url_to_mortgage_statement>
"""

import sys
import os
import json
import argparse
from dotenv import load_dotenv
from mortgage_parser import MortgageStatementParser


def load_credentials():
    """Load Veryfi credentials from environment variables."""
    load_dotenv()
    
    client_id = os.getenv('VERYFI_CLIENT_ID')
    client_secret = os.getenv('VERYFI_CLIENT_SECRET')
    username = os.getenv('VERYFI_USERNAME')
    api_key = os.getenv('VERYFI_API_KEY')
    
    if not all([client_id, client_secret, username, api_key]):
        raise ValueError(
            "Missing Veryfi credentials. Please set the following environment variables:\n"
            "VERYFI_CLIENT_ID, VERYFI_CLIENT_SECRET, VERYFI_USERNAME, VERYFI_API_KEY\n"
            "You can copy .env.example to .env and fill in your credentials."
        )
    
    return client_id, client_secret, username, api_key


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Parse mortgage statements using Veryfi SDK',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Parse a local file:
    python app.py statement.pdf
    python app.py statement.jpg
  
  Parse from URL:
    python app.py --url https://example.com/statement.pdf
  
  Save output to JSON:
    python app.py statement.pdf --output result.json
        """
    )
    
    parser.add_argument(
        'file_path',
        nargs='?',
        help='Path to the mortgage statement file (image or PDF)'
    )
    parser.add_argument(
        '--url',
        help='URL of the mortgage statement to parse'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path for JSON results (optional)'
    )
    parser.add_argument(
        '--raw',
        action='store_true',
        help='Show raw Veryfi response'
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not args.file_path and not args.url:
        parser.error("Please provide either a file path or --url")
    
    if args.file_path and args.url:
        parser.error("Please provide either a file path or --url, not both")
    
    try:
        # Load credentials
        print("Loading Veryfi credentials...")
        client_id, client_secret, username, api_key = load_credentials()
        
        # Initialize parser
        print("Initializing mortgage parser...")
        parser_instance = MortgageStatementParser(
            client_id, client_secret, username, api_key
        )
        
        # Parse the document
        if args.file_path:
            print(f"Processing file: {args.file_path}")
            result = parser_instance.parse_mortgage_statement(args.file_path)
        else:
            print(f"Processing URL: {args.url}")
            result = parser_instance.parse_mortgage_statement_from_url(args.url)
        
        print("\n" + "="*50)
        print("Processing complete!")
        print("="*50 + "\n")
        
        # Display results
        if args.raw:
            print("=== RAW VERYFI RESPONSE ===")
            print(json.dumps(result.get('raw_response', {}), indent=2))
        else:
            print(parser_instance.format_output(result))
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to: {args.output}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing document: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
