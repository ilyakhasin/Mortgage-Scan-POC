# Mortgage-Scan-POC

A proof-of-concept application for scanning and parsing mortgage statements using the Veryfi SDK. Point your phone at a mortgage statement, and this tool will extract key information including loan amounts, APR, terms, property address, and important dates.

## Features

- 📱 **Mobile-Friendly**: Scan mortgage statements directly from your phone camera
- 🔍 **Smart Parsing**: Extracts key mortgage information using Veryfi's OCR API
- 📊 **Comprehensive Data Extraction**:
  - Original loan amount
  - Outstanding balance
  - Annual Percentage Rate (APR)
  - Loan terms (e.g., 30-year fixed)
  - Property address
  - Payment dates and due dates
  - Lender information
- 💾 **Multiple Input Methods**: Support for local files, URLs, and direct image upload
- 📄 **Format Support**: Works with PDF, JPG, PNG, and other common image formats

## Prerequisites

- Python 3.7 or higher
- Veryfi API account (get one at [https://hub.veryfi.com](https://hub.veryfi.com))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ilyakhasin/Mortgage-Scan-POC.git
cd Mortgage-Scan-POC
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Veryfi credentials:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Veryfi API credentials:
```
VERYFI_CLIENT_ID=your_client_id_here
VERYFI_CLIENT_SECRET=your_client_secret_here
VERYFI_USERNAME=your_username_here
VERYFI_API_KEY=your_api_key_here
```

You can get your credentials from [Veryfi Hub API Settings](https://hub.veryfi.com/api/settings/keys/).

## Usage

### Command Line Interface

Parse a local mortgage statement file:
```bash
python app.py statement.pdf
```

Parse from a URL:
```bash
python app.py --url https://example.com/mortgage-statement.pdf
```

Save results to JSON file:
```bash
python app.py statement.jpg --output results.json
```

View raw Veryfi response:
```bash
python app.py statement.pdf --raw
```

### Python API

```python
from mortgage_parser import MortgageStatementParser

# Initialize parser with credentials
parser = MortgageStatementParser(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_username",
    api_key="your_api_key"
)

# Parse a mortgage statement
result = parser.parse_mortgage_statement("statement.pdf")

# Access parsed fields
parsed = result['parsed_fields']
print(f"Outstanding Balance: ${parsed['outstanding_balance']}")
print(f"APR: {parsed['apr']}%")
print(f"Property Address: {parsed['property_address']}")

# Format output
print(parser.format_output(result))
```

## Example Output

```
=== Mortgage Statement Summary ===

Lender: ABC Mortgage Company
Original Loan Amount: $350,000.00
Outstanding Balance: $287,450.23
APR: 3.75%
Loan Terms: 30 year fixed
Property Address: 123 Main Street, Anytown, ST 12345
Payment Amount: $1,620.50

=== Important Dates ===
Statement Date: 2024-01-15
Due Date: 2024-02-01
Payment Date: 2024-01-20

Confidence Score: 0.98
```

## How It Works

1. **Document Upload**: The application accepts mortgage statement images or PDFs
2. **OCR Processing**: Veryfi's powerful OCR engine extracts text and structure from the document
3. **Field Extraction**: Custom parsing logic identifies and extracts mortgage-specific fields:
   - Pattern matching for APR and loan terms
   - Line item analysis for loan amounts and balances
   - Address extraction from vendor/property fields
   - Date parsing for statement and payment dates
4. **Structured Output**: Returns organized data in JSON format with high confidence scores

## Extracted Fields

| Field | Description |
|-------|-------------|
| `loan_amount` | Original loan amount at origination |
| `outstanding_balance` | Current principal balance remaining |
| `apr` | Annual Percentage Rate |
| `loan_terms` | Term length (e.g., "30 year fixed") |
| `property_address` | Address of the mortgaged property |
| `payment_amount` | Current payment amount |
| `lender_name` | Name of the lending institution |
| `dates.statement_date` | Date of the statement |
| `dates.due_date` | Payment due date |
| `dates.payment_date` | Last payment date |
| `dates.loan_origination_date` | Original loan date |

## Project Structure

```
Mortgage-Scan-POC/
├── app.py                  # Main CLI application
├── mortgage_parser.py      # Core parsing logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## API Reference

### MortgageStatementParser

Main class for parsing mortgage statements.

#### Methods

- `__init__(client_id, client_secret, username, api_key)`: Initialize with Veryfi credentials
- `parse_mortgage_statement(file_path)`: Parse a local file
- `parse_mortgage_statement_from_url(file_url)`: Parse from URL
- `format_output(mortgage_data)`: Format parsed data as readable text

## Troubleshooting

### Missing Credentials Error
If you see "Missing Veryfi credentials", ensure your `.env` file exists and contains valid credentials.

### File Not Found Error
Make sure the file path is correct and the file exists. Use absolute paths if needed.

### API Rate Limits
Free Veryfi accounts have usage limits. Check your [Veryfi dashboard](https://hub.veryfi.com) for current usage.

## Future Enhancements

- [ ] Web interface for uploading statements
- [ ] Mobile app integration
- [ ] Batch processing support
- [ ] Historical data tracking
- [ ] Payment schedule extraction
- [ ] Escrow account details
- [ ] Multi-lender support
- [ ] Export to spreadsheet formats

## Security Notes

- Never commit your `.env` file or expose API credentials
- The `.gitignore` file is configured to exclude credentials
- Keep your Veryfi API keys secure and rotate them regularly

## License

This is a proof-of-concept project. Please ensure compliance with Veryfi's terms of service when using their API.

## Contributing

This is a POC project. Feel free to fork and enhance for your needs.

## Support

For Veryfi API issues, contact [Veryfi Support](https://www.veryfi.com/support/)

For project-specific questions, please open an issue on GitHub.