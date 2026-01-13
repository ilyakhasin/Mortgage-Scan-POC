"""
Mortgage Statement Parser using Veryfi SDK

This module provides functionality to scan and parse mortgage statements
using the Veryfi OCR API. It extracts key information such as loan amounts,
APR, terms, property address, and dates.
"""

import os
import json
import re
from typing import Dict, Optional, Any
from veryfi import Client


class MortgageStatementParser:
    """
    Parser for mortgage statements using Veryfi SDK.
    
    Extracts key mortgage information including:
    - Loan amount
    - Outstanding loan amount
    - APR (Annual Percentage Rate)
    - Terms of the loan
    - Property address
    - Relevant dates
    """
    
    def __init__(self, client_id: str, client_secret: str, username: str, api_key: str):
        """
        Initialize the Veryfi client with credentials.
        
        Args:
            client_id: Veryfi client ID
            client_secret: Veryfi client secret
            username: Veryfi username
            api_key: Veryfi API key
        """
        self.client = Client(client_id, client_secret, username, api_key)
        
    def parse_mortgage_statement(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a mortgage statement from an image or PDF file.
        
        Args:
            file_path: Path to the mortgage statement file
            
        Returns:
            Dictionary containing parsed mortgage information
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            Exception: If parsing fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Process document with Veryfi
        categories = ['mortgage', 'financial', 'bank statement']
        response = self.client.process_document(file_path, categories=categories)
        
        # Extract mortgage-specific fields
        mortgage_data = self._extract_mortgage_fields(response)
        
        return mortgage_data
    
    def parse_mortgage_statement_from_url(self, file_url: str) -> Dict[str, Any]:
        """
        Parse a mortgage statement from a URL.
        
        Args:
            file_url: URL of the mortgage statement
            
        Returns:
            Dictionary containing parsed mortgage information
        """
        categories = ['mortgage', 'financial', 'bank statement']
        response = self.client.process_document_url(file_url, categories=categories)
        
        mortgage_data = self._extract_mortgage_fields(response)
        
        return mortgage_data
    
    def _extract_mortgage_fields(self, veryfi_response: Dict) -> Dict[str, Any]:
        """
        Extract mortgage-specific fields from Veryfi response.
        
        Args:
            veryfi_response: Raw response from Veryfi API
            
        Returns:
            Dictionary with structured mortgage data
        """
        # Extract text content for parsing
        text_content = veryfi_response.get('ocr_text', '')
        line_items = veryfi_response.get('line_items', [])
        
        # Initialize mortgage data structure
        mortgage_data = {
            'raw_response': veryfi_response,
            'parsed_fields': {
                'loan_amount': self._extract_loan_amount(veryfi_response),
                'outstanding_balance': self._extract_outstanding_balance(veryfi_response),
                'apr': self._extract_apr(veryfi_response),
                'loan_terms': self._extract_loan_terms(veryfi_response),
                'property_address': self._extract_property_address(veryfi_response),
                'dates': self._extract_dates(veryfi_response),
                'payment_amount': veryfi_response.get('total', None),
                'lender_name': veryfi_response.get('vendor', {}).get('name', None),
            },
            'confidence_score': veryfi_response.get('confidence', None),
            'document_type': veryfi_response.get('document_type', None),
        }
        
        return mortgage_data
    
    def _extract_loan_amount(self, response: Dict) -> Optional[float]:
        """Extract original loan amount from the response."""
        # Check line items for loan amount
        for item in response.get('line_items', []):
            description = str(item.get('description', '')).lower()
            if 'original loan' in description or 'loan amount' in description:
                return item.get('total', None)
        
        # Check custom fields
        for field in response.get('custom_fields', []):
            if 'loan amount' in str(field.get('name', '')).lower():
                return field.get('value', None)
        
        return None
    
    def _extract_outstanding_balance(self, response: Dict) -> Optional[float]:
        """Extract outstanding/principal balance from the response."""
        # Check for principal balance or outstanding balance
        for item in response.get('line_items', []):
            description = str(item.get('description', '')).lower()
            if any(term in description for term in ['principal balance', 'outstanding balance', 
                                                      'current balance', 'remaining balance']):
                return item.get('total', None)
        
        # Check total field as fallback
        total = response.get('total', None)
        if total and total > 0:
            return total
        
        return None
    
    def _extract_apr(self, response: Dict) -> Optional[float]:
        """Extract APR (Annual Percentage Rate) from the response."""
        text = response.get('ocr_text', '').lower()
        
        # Look for APR patterns in text
        apr_patterns = [
            r'apr[:\s]+(\d+\.?\d*)\s*%?',
            r'annual percentage rate[:\s]+(\d+\.?\d*)\s*%?',
            r'interest rate[:\s]+(\d+\.?\d*)\s*%?',
        ]
        
        for pattern in apr_patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))
        
        # Check custom fields
        for field in response.get('custom_fields', []):
            field_name = str(field.get('name', '')).lower()
            if 'apr' in field_name or 'interest rate' in field_name:
                value = field.get('value', None)
                if value:
                    try:
                        return float(str(value).replace('%', ''))
                    except ValueError:
                        pass
        
        return None
    
    def _extract_loan_terms(self, response: Dict) -> Optional[str]:
        """Extract loan terms (e.g., '30 years', '15 years') from the response."""
        text = response.get('ocr_text', '').lower()
        
        # Look for term patterns
        term_patterns = [
            r'(\d+)\s*year\s*(?:fixed|term|loan)?',
            r'(\d+)\s*month\s*(?:term|loan)?',
            r'loan term[:\s]+(\d+\s*(?:year|month)s?)',
        ]
        
        for pattern in term_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).strip()
        
        return None
    
    def _extract_property_address(self, response: Dict) -> Optional[str]:
        """Extract property address from the response."""
        # Check vendor/bill to address
        vendor = response.get('vendor', {})
        if vendor:
            address = vendor.get('address', None)
            if address:
                return address
        
        # Check bill_to field
        bill_to = response.get('bill_to', {})
        if bill_to:
            address = bill_to.get('address', None)
            if address:
                return address
        
        # Look in OCR text for address patterns
        text = response.get('ocr_text', '')
        # Simple address pattern (can be enhanced)
        address_pattern = r'property(?:\s+address)?[:\s]+([^\n]+(?:\n[^\n]+)?)'
        match = re.search(address_pattern, text.lower())
        if match:
            return match.group(1).strip()
        
        return None
    
    def _extract_dates(self, response: Dict) -> Dict[str, Optional[str]]:
        """Extract relevant dates from the response."""
        dates = {
            'statement_date': response.get('date', None),
            'due_date': response.get('due_date', None),
            'payment_date': None,
            'loan_origination_date': None,
        }
        
        # Look for additional dates in OCR text
        text = response.get('ocr_text', '').lower()
        
        # Payment date pattern
        payment_match = re.search(r'payment date[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
        if payment_match:
            dates['payment_date'] = payment_match.group(1)
        
        # Loan origination date pattern
        origin_match = re.search(r'(?:loan|origination) date[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
        if origin_match:
            dates['loan_origination_date'] = origin_match.group(1)
        
        return dates
    
    def format_output(self, mortgage_data: Dict) -> str:
        """
        Format the parsed mortgage data into a readable string.
        
        Args:
            mortgage_data: Parsed mortgage data dictionary
            
        Returns:
            Formatted string representation
        """
        parsed = mortgage_data.get('parsed_fields', {})
        
        output = "=== Mortgage Statement Summary ===\n\n"
        
        if parsed.get('lender_name'):
            output += f"Lender: {parsed['lender_name']}\n"
        
        if parsed.get('loan_amount'):
            output += f"Original Loan Amount: ${parsed['loan_amount']:,.2f}\n"
        
        if parsed.get('outstanding_balance'):
            output += f"Outstanding Balance: ${parsed['outstanding_balance']:,.2f}\n"
        
        if parsed.get('apr'):
            output += f"APR: {parsed['apr']}%\n"
        
        if parsed.get('loan_terms'):
            output += f"Loan Terms: {parsed['loan_terms']}\n"
        
        if parsed.get('property_address'):
            output += f"Property Address: {parsed['property_address']}\n"
        
        if parsed.get('payment_amount'):
            output += f"Payment Amount: ${parsed['payment_amount']:,.2f}\n"
        
        dates = parsed.get('dates', {})
        if dates:
            output += "\n=== Important Dates ===\n"
            for date_type, date_value in dates.items():
                if date_value:
                    formatted_type = date_type.replace('_', ' ').title()
                    output += f"{formatted_type}: {date_value}\n"
        
        confidence = mortgage_data.get('confidence_score')
        if confidence:
            output += f"\nConfidence Score: {confidence}\n"
        
        return output
