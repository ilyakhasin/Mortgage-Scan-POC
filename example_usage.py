"""
Example usage script for the Mortgage Statement Parser

This script demonstrates how to use the MortgageStatementParser class
in your own Python code.
"""

import os
from dotenv import load_dotenv
from mortgage_parser import MortgageStatementParser


def example_parse_local_file():
    """Example: Parse a local mortgage statement file"""
    print("Example 1: Parsing a local file\n" + "="*50)
    
    # Load credentials from .env file
    load_dotenv()
    
    # Initialize the parser
    parser = MortgageStatementParser(
        client_id=os.getenv('VERYFI_CLIENT_ID'),
        client_secret=os.getenv('VERYFI_CLIENT_SECRET'),
        username=os.getenv('VERYFI_USERNAME'),
        api_key=os.getenv('VERYFI_API_KEY')
    )
    
    # Parse a mortgage statement
    # Replace with your actual file path
    file_path = "path/to/your/mortgage_statement.pdf"
    
    try:
        result = parser.parse_mortgage_statement(file_path)
        
        # Display formatted output
        print(parser.format_output(result))
        
        # Access specific fields
        parsed = result['parsed_fields']
        print("\nAccessing specific fields:")
        print(f"Outstanding Balance: ${parsed.get('outstanding_balance', 'N/A')}")
        print(f"APR: {parsed.get('apr', 'N/A')}%")
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        print("Please update the file_path variable with your actual mortgage statement.")
    except Exception as e:
        print(f"Error: {e}")


def example_parse_from_url():
    """Example: Parse a mortgage statement from a URL"""
    print("\n\nExample 2: Parsing from URL\n" + "="*50)
    
    load_dotenv()
    
    parser = MortgageStatementParser(
        client_id=os.getenv('VERYFI_CLIENT_ID'),
        client_secret=os.getenv('VERYFI_CLIENT_SECRET'),
        username=os.getenv('VERYFI_USERNAME'),
        api_key=os.getenv('VERYFI_API_KEY')
    )
    
    # Parse from URL
    # Replace with your actual URL
    url = "https://example.com/mortgage_statement.pdf"
    
    try:
        result = parser.parse_mortgage_statement_from_url(url)
        print(parser.format_output(result))
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please update the url variable with your actual mortgage statement URL.")


def example_custom_processing():
    """Example: Custom processing of parsed data"""
    print("\n\nExample 3: Custom data processing\n" + "="*50)
    
    load_dotenv()
    
    parser = MortgageStatementParser(
        client_id=os.getenv('VERYFI_CLIENT_ID'),
        client_secret=os.getenv('VERYFI_CLIENT_SECRET'),
        username=os.getenv('VERYFI_USERNAME'),
        api_key=os.getenv('VERYFI_API_KEY')
    )
    
    file_path = "path/to/your/mortgage_statement.pdf"
    
    try:
        result = parser.parse_mortgage_statement(file_path)
        parsed = result['parsed_fields']
        
        # Example: Calculate equity if we have loan amount and balance
        loan_amount = parsed.get('loan_amount')
        outstanding = parsed.get('outstanding_balance')
        
        if loan_amount and outstanding:
            principal_paid = loan_amount - outstanding
            equity_percentage = (principal_paid / loan_amount) * 100
            
            print(f"Loan Analysis:")
            print(f"  Original Loan: ${loan_amount:,.2f}")
            print(f"  Current Balance: ${outstanding:,.2f}")
            print(f"  Principal Paid: ${principal_paid:,.2f}")
            print(f"  Equity Built: {equity_percentage:.2f}%")
        
        # Example: Check if APR is competitive
        apr = parsed.get('apr')
        if apr:
            if apr < 3.0:
                rate_status = "Excellent"
            elif apr < 4.0:
                rate_status = "Good"
            elif apr < 5.0:
                rate_status = "Fair"
            else:
                rate_status = "Consider refinancing"
            
            print(f"\nRate Assessment: {rate_status} (APR: {apr}%)")
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        print("Please update the file_path variable with your actual mortgage statement.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples"""
    print("Mortgage Statement Parser - Usage Examples")
    print("="*50)
    print()
    
    # Check if credentials are set
    load_dotenv()
    if not all([
        os.getenv('VERYFI_CLIENT_ID'),
        os.getenv('VERYFI_CLIENT_SECRET'),
        os.getenv('VERYFI_USERNAME'),
        os.getenv('VERYFI_API_KEY')
    ]):
        print("ERROR: Veryfi credentials not found!")
        print("Please copy .env.example to .env and fill in your credentials.")
        return
    
    print("Note: These examples require actual mortgage statement files.")
    print("Update the file paths in this script to test with your own files.\n")
    
    # Uncomment the examples you want to run:
    # example_parse_local_file()
    # example_parse_from_url()
    # example_custom_processing()
    
    print("\nTo use these examples:")
    print("1. Uncomment the example function calls above")
    print("2. Update file paths or URLs with your actual documents")
    print("3. Run: python example_usage.py")


if __name__ == '__main__':
    main()
