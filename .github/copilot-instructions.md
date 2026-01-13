# Copilot Instructions for Mortgage-Scan-POC

## Project Overview

This is a proof-of-concept Python application that scans and parses mortgage statements using the Veryfi OCR API. The project extracts key mortgage information such as loan amounts, APR, property addresses, and dates from document images or PDFs.

**Primary Goal:** Validate the feasibility of mobile-based mortgage document extraction using off-the-shelf Intelligent Document Processing (IDP) solutions.

## Technology Stack

- **Language:** Python 3.x
- **Key Dependencies:**
  - `veryfi==3.3.2` - Veryfi SDK for OCR processing
  - `python-dotenv==1.0.0` - Environment variable management
- **API Integration:** Veryfi Bank Statement API
- **Planned Mobile Integration:** React Native with Veryfi Lens SDK (per Architecture Doc)

## Project Structure

- `mortgage_parser.py` - Core parser class (`MortgageStatementParser`)
- `app.py` - CLI application for parsing mortgage statements
- `example_usage.py` - Usage examples and integration patterns
- `test_parser.py` - Unit tests (run with `python test_parser.py`)
- `.env.example` - Template for Veryfi API credentials
- `Architecture Doc` - System design and data flow documentation

## Code Conventions

### Python Style
- Use docstrings for all modules, classes, and functions
- Follow existing docstring format (Google style)
- Use type hints for function parameters and return values
- Private methods are prefixed with underscore (e.g., `_extract_loan_amount`)

### Naming Conventions
- Classes: PascalCase (e.g., `MortgageStatementParser`)
- Functions/Methods: snake_case (e.g., `parse_mortgage_statement`)
- Constants: UPPER_SNAKE_CASE (e.g., `VERYFI_CLIENT_ID`)

### Code Organization
- Keep extraction logic in private methods (e.g., `_extract_apr`, `_extract_dates`)
- Main parsing methods should orchestrate extraction and return structured data
- Use the `format_output` method for user-friendly display formatting

## Testing Practices

- Tests are located in `test_parser.py`
- Run tests with: `python test_parser.py`
- Tests use mock data to avoid requiring actual API credentials
- All extraction methods should be tested with sample Veryfi responses
- Tests verify:
  - Module imports
  - Parser initialization
  - Method existence
  - Output formatting
  - Field extraction logic

### Test Structure
- Test functions are named `test_<functionality>`
- Use try/except blocks with descriptive error messages
- Return boolean success/failure for aggregation

## Environment Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API credentials:**
   - Copy `.env.example` to `.env`
   - Fill in Veryfi API credentials from https://hub.veryfi.com/api/settings/keys/
   - Required variables: `VERYFI_CLIENT_ID`, `VERYFI_CLIENT_SECRET`, `VERYFI_USERNAME`, `VERYFI_API_KEY`

3. **Run tests:**
   ```bash
   python test_parser.py
   ```

## Usage Patterns

### Basic Usage
```bash
# Parse local file
python app.py statement.pdf

# Parse from URL
python app.py --url https://example.com/statement.pdf

# Save output to JSON
python app.py statement.pdf --output result.json
```

### Programmatic Usage
```python
from mortgage_parser import MortgageStatementParser

parser = MortgageStatementParser(client_id, client_secret, username, api_key)
result = parser.parse_mortgage_statement("statement.pdf")
```

## Key Extracted Fields

The parser extracts and structures the following mortgage data:
- `lender_name` - Mortgage lender/servicer name
- `loan_amount` - Original loan amount
- `outstanding_balance` - Current principal balance
- `apr` - Annual Percentage Rate
- `loan_terms` - Loan duration and type (e.g., "30 year fixed")
- `property_address` - Property address for the mortgage
- `payment_amount` - Monthly payment amount
- `dates` - Statement date, due date, and other relevant dates

## Security Considerations

- **Never commit API credentials** - Use `.env` files (already in `.gitignore`)
- **Sensitive document handling:**
  - Test images and PDFs are excluded from git (`.gitignore` includes `*.jpg`, `*.png`, `*.pdf`)
  - No raw document images should be stored post-processing unless user opts in
- **Data encryption:** All API communications use TLS 1.3
- **Credentials validation:** App validates all required credentials before processing

## Future Architecture Notes

Per the Architecture Doc, this Python POC validates the extraction logic. The planned production system will:
- Use React Native with Veryfi Lens SDK for mobile capture
- Implement TurboModules for high-performance camera processing
- Use Context API or Zustand for state management
- Store data in SQLite/WatermelonDB
- Provide an editable UI with pre-filled form components

## When Making Changes

1. **Adding new extraction fields:**
   - Create a private `_extract_<field_name>` method
   - Call it from `_extract_mortgage_fields`
   - Add to output structure in `format_output`
   - Add test case in `test_parser.py`

2. **Modifying existing logic:**
   - Ensure backward compatibility with existing field names
   - Update tests to reflect new behavior
   - Update docstrings to document changes

3. **Adding new features:**
   - Follow existing patterns (e.g., argparse for CLI, dotenv for config)
   - Add example usage to `example_usage.py`
   - Document in relevant docstrings

4. **Dependencies:**
   - Add to `requirements.txt` with version pinning
   - Document purpose in comments if not obvious
