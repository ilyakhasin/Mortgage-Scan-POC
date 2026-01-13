"""
Basic tests for the Mortgage Statement Parser

Run with: python test_parser.py
"""

import sys


def test_imports():
    """Test that all modules can be imported"""
    print("Test 1: Testing imports...")
    try:
        from mortgage_parser import MortgageStatementParser
        print("✓ mortgage_parser module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False


def test_parser_initialization():
    """Test that parser can be initialized"""
    print("\nTest 2: Testing parser initialization...")
    try:
        from mortgage_parser import MortgageStatementParser
        
        # Initialize with dummy credentials
        parser = MortgageStatementParser(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            api_key="test_key"
        )
        print("✓ Parser initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize parser: {e}")
        return False


def test_field_extraction_methods():
    """Test that field extraction methods exist"""
    print("\nTest 3: Testing field extraction methods...")
    try:
        from mortgage_parser import MortgageStatementParser
        
        parser = MortgageStatementParser(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            api_key="test_key"
        )
        
        # Check that extraction methods exist
        methods = [
            '_extract_loan_amount',
            '_extract_outstanding_balance',
            '_extract_apr',
            '_extract_loan_terms',
            '_extract_property_address',
            '_extract_dates',
            '_extract_mortgage_fields',
            'format_output'
        ]
        
        for method in methods:
            if not hasattr(parser, method):
                print(f"✗ Missing method: {method}")
                return False
        
        print(f"✓ All {len(methods)} expected methods found")
        return True
    except Exception as e:
        print(f"✗ Error checking methods: {e}")
        return False


def test_format_output():
    """Test the format_output method with sample data"""
    print("\nTest 4: Testing format_output method...")
    try:
        from mortgage_parser import MortgageStatementParser
        
        parser = MortgageStatementParser(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            api_key="test_key"
        )
        
        # Create sample mortgage data
        sample_data = {
            'parsed_fields': {
                'lender_name': 'Test Bank',
                'loan_amount': 350000.00,
                'outstanding_balance': 287450.23,
                'apr': 3.75,
                'loan_terms': '30 year fixed',
                'property_address': '123 Main St, Anytown, ST 12345',
                'payment_amount': 1620.50,
                'dates': {
                    'statement_date': '2024-01-15',
                    'due_date': '2024-02-01'
                }
            },
            'confidence_score': 0.98
        }
        
        output = parser.format_output(sample_data)
        
        # Check that output contains expected fields
        expected_strings = [
            'Test Bank',
            '$350,000.00',
            '$287,450.23',
            '3.75%',
            '30 year fixed',
            '123 Main St'
        ]
        
        for expected in expected_strings:
            if expected not in output:
                print(f"✗ Expected string not found in output: {expected}")
                return False
        
        print("✓ format_output produces correct output")
        return True
    except Exception as e:
        print(f"✗ Error testing format_output: {e}")
        return False


def test_extraction_with_mock_data():
    """Test field extraction with mock Veryfi response"""
    print("\nTest 5: Testing field extraction with mock data...")
    try:
        from mortgage_parser import MortgageStatementParser
        
        parser = MortgageStatementParser(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            api_key="test_key"
        )
        
        # Mock Veryfi response
        mock_response = {
            'ocr_text': 'APR: 3.75% Loan Term: 30 year fixed',
            'total': 287450.23,
            'date': '2024-01-15',
            'due_date': '2024-02-01',
            'vendor': {
                'name': 'Test Mortgage Co.',
                'address': '456 Bank St, Finance City, ST 67890'
            },
            'line_items': [
                {
                    'description': 'Principal Balance',
                    'total': 287450.23
                }
            ],
            'confidence': 0.95,
            'custom_fields': []
        }
        
        result = parser._extract_mortgage_fields(mock_response)
        
        # Verify structure
        if 'parsed_fields' not in result:
            print("✗ Missing parsed_fields in result")
            return False
        
        parsed = result['parsed_fields']
        
        # Check that APR was extracted
        if parsed['apr'] == 3.75:
            print("✓ APR extracted correctly: 3.75%")
        else:
            print(f"✗ APR extraction failed. Got: {parsed['apr']}")
            return False
        
        # Check that outstanding balance was extracted
        if parsed['outstanding_balance'] == 287450.23:
            print("✓ Outstanding balance extracted correctly: $287,450.23")
        else:
            print(f"✗ Balance extraction failed. Got: {parsed['outstanding_balance']}")
            return False
        
        # Check that loan terms were extracted
        if '30 year' in str(parsed['loan_terms']):
            print("✓ Loan terms extracted correctly")
        else:
            print(f"✗ Loan terms extraction failed. Got: {parsed['loan_terms']}")
        
        print("✓ Field extraction works with mock data")
        return True
        
    except Exception as e:
        print(f"✗ Error testing extraction: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("Mortgage Statement Parser - Unit Tests")
    print("="*60)
    
    tests = [
        test_imports,
        test_parser_initialization,
        test_field_extraction_methods,
        test_format_output,
        test_extraction_with_mock_data
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
