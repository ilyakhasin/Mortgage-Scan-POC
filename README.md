# Mortgage Statement Parser - PoC

A Python-based proof-of-concept tool that parses mortgage statements using AI-powered OCR. This tool demonstrates high-accuracy data extraction from financial documents using the Veryfi SDK.

## 📋 Overview

This repository contains a **Python command-line application** that extracts structured data from mortgage statements (PDF or images). It uses the Veryfi OCR API to automatically identify and parse key mortgage information such as loan amounts, APR, property addresses, payment dates, and more.

**Note:** The `Architecture Doc` file describes a future React Native mobile application concept. The current implementation is a Python-based command-line tool that serves as a foundation for understanding mortgage document parsing.

## ✨ What This Software Does

The Mortgage Statement Parser:
1. **Accepts** mortgage statement documents (PDF, JPG, PNG) via file path or URL
2. **Processes** them using Veryfi's AI-powered OCR service
3. **Extracts** key mortgage data:
   - Original loan amount
   - Outstanding/principal balance
   - APR (Annual Percentage Rate)
   - Loan terms (e.g., "30 year fixed")
   - Property address
   - Important dates (statement date, due date, payment date)
   - Lender information
   - Payment amounts
4. **Returns** structured JSON data or formatted text output
5. **Provides** confidence scores for the extracted data

## 🚀 Key Features

- **AI-Powered Extraction:** Uses Veryfi's intelligent document processing
- **Multiple Input Methods:** Process local files or documents from URLs
- **Flexible Output:** View formatted summaries or raw JSON data
- **High Accuracy:** Extracts specific mortgage fields with confidence scoring
- **Easy Integration:** Simple Python API for embedding in other applications

## 🛠️ Prerequisites

- Python 3.7 or higher
- Veryfi API credentials (free tier available at https://hub.veryfi.com/)
- pip (Python package manager)

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ilyakhasin/Mortgage-Scan-POC.git
cd Mortgage-Scan-POC
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `veryfi` - Veryfi SDK for OCR processing (v3.3.0 or higher)
- `python-dotenv` - Environment variable management (v1.0.0 or higher)

### 3. Set Up API Credentials

1. Sign up for a free Veryfi account at https://hub.veryfi.com/
2. Get your API credentials from https://hub.veryfi.com/api/settings/keys/
3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and add your credentials:
   ```
   VERYFI_CLIENT_ID=your_client_id_here
   VERYFI_CLIENT_SECRET=your_client_secret_here
   VERYFI_USERNAME=your_username_here
   VERYFI_API_KEY=your_api_key_here
   ```

## 🎯 How to Run It

### Basic Usage - Parse a Local File

```bash
python app.py path/to/mortgage_statement.pdf
```

Or with an image:
```bash
python app.py path/to/mortgage_statement.jpg
```

### Parse from a URL

```bash
python app.py --url https://example.com/mortgage_statement.pdf
```

### Save Output to JSON File

```bash
python app.py statement.pdf --output results.json
```

### View Raw API Response

```bash
python app.py statement.pdf --raw
```

### Example Output

When you run the parser, you'll see output like this:

```
Loading Veryfi credentials...
Initializing mortgage parser...
Processing file: statement.pdf

==================================================
Processing complete!
==================================================

=== Mortgage Statement Summary ===

Lender: ABC Mortgage Company
Original Loan Amount: $350,000.00
Outstanding Balance: $287,450.23
APR: 3.75%
Loan Terms: 30 year fixed
Property Address: 123 Main St, Anytown, ST 12345
Payment Amount: $1,620.50

=== Important Dates ===
Statement Date: 2024-01-15
Due Date: 2024-02-01

Confidence Score: 0.98
```

## 📁 Repository Structure

```
Mortgage-Scan-POC/
│
├── app.py                  # Main CLI application entry point
├── mortgage_parser.py      # Core parser class with extraction logic
├── example_usage.py        # Example code showing how to use the parser
├── test_parser.py          # Unit tests for the parser
│
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables file
├── .gitignore            # Git ignore rules
│
├── README.md             # This file
└── Architecture Doc      # Future mobile app architecture (conceptual)
```

## 🔧 Using the Parser in Your Code

You can import and use the parser in your own Python scripts:

```python
from mortgage_parser import MortgageStatementParser
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()

# Initialize parser
parser = MortgageStatementParser(
    client_id=os.getenv('VERYFI_CLIENT_ID'),
    client_secret=os.getenv('VERYFI_CLIENT_SECRET'),
    username=os.getenv('VERYFI_USERNAME'),
    api_key=os.getenv('VERYFI_API_KEY')
)

# Parse a document
result = parser.parse_mortgage_statement('statement.pdf')

# Access parsed data
parsed = result['parsed_fields']
print(f"Loan Balance: ${parsed['outstanding_balance']}")
print(f"APR: {parsed['apr']}%")

# Or use formatted output
print(parser.format_output(result))
```

See `example_usage.py` for more detailed examples.

## 🧪 Running Tests

Run the included unit tests to verify the installation:

```bash
python test_parser.py
```

The tests verify:
- Module imports work correctly
- Parser initializes properly
- Field extraction methods exist
- Output formatting works
- Mock data extraction functions correctly

## 📊 What Data Gets Extracted

The parser attempts to extract the following fields from mortgage statements:

| Field | Description | Example |
|-------|-------------|---------|
| `loan_amount` | Original loan amount | $350,000.00 |
| `outstanding_balance` | Current principal balance | $287,450.23 |
| `apr` | Annual percentage rate | 3.75 |
| `loan_terms` | Loan duration and type | "30 year fixed" |
| `property_address` | Property location | "123 Main St, Anytown, ST" |
| `payment_amount` | Monthly payment amount | $1,620.50 |
| `lender_name` | Mortgage company name | "ABC Mortgage Company" |
| `dates` | Statement, due, payment dates | Various date formats |
| `confidence_score` | Extraction confidence (0-1) | 0.98 |

## 🔐 Security & Privacy

- All API communication uses HTTPS/TLS encryption
- Credentials are stored in `.env` files (excluded from git)
- No documents are stored permanently by this tool
- Veryfi's security policies apply to API processing

## 🐛 Troubleshooting

### "Missing Veryfi credentials" Error
- Make sure you've created a `.env` file (copy from `.env.example`)
- Verify all four credentials are set in the `.env` file
- Check that the `.env` file is in the same directory as `app.py`

### "File not found" Error
- Verify the file path is correct
- Use absolute paths or paths relative to where you run the script
- Check that the file exists and you have read permissions

### Import Errors
- Ensure you've installed dependencies: `pip install -r requirements.txt`
- Verify you're using Python 3.7+: `python --version`

### API Errors
- Check that your Veryfi API credentials are valid
- Verify your API quota hasn't been exceeded (check Veryfi dashboard)
- Ensure you have an active internet connection

## 📚 Additional Resources

- **Veryfi Documentation:** https://docs.veryfi.com/
- **Veryfi Python SDK:** https://github.com/veryfi/veryfi-python
- **Get API Credentials:** https://hub.veryfi.com/api/settings/keys/

## 🗺️ Future Development

The `Architecture Doc` file outlines a vision for a React Native mobile application that would:
- Provide a native mobile scanning experience
- Use Veryfi Lens SDK for camera integration
- Offer real-time document scanning with edge detection
- Include an editable form UI for user verification
- Support the new React Native architecture (Fabric/TurboModules)

This Python tool serves as a proof-of-concept for the document parsing capabilities that would power such a mobile app.

## 📄 License

This is a proof-of-concept project. Check with the repository owner for licensing information.

## 🤝 Contributing

This is a proof-of-concept repository. For questions or contributions, please contact the repository owner.

---

**Quick Start Summary:**
1. Install Python 3.7+
2. Run `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your Veryfi credentials
4. Run `python app.py your_mortgage_statement.pdf`
