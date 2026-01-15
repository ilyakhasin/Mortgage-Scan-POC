# Repository Summary - Mortgage-Scan-POC

## Quick Overview

**What is this?** A Python command-line tool that uses AI (Veryfi OCR API) to extract structured data from mortgage statements.

**What does it do?** Converts mortgage PDFs/images into structured data (loan amounts, APR, addresses, dates, etc.)

**How do I run it?** 
1. Install Python packages: `pip install -r requirements.txt`
2. Get free Veryfi API credentials and add to `.env` file
3. Run: `python app.py your_statement.pdf`

## Repository Contents

### Core Application Files
- **`app.py`** - Main CLI application (run this to process documents)
- **`mortgage_parser.py`** - Core parsing logic and field extraction
- **`example_usage.py`** - Code examples showing how to use the parser
- **`test_parser.py`** - Unit tests (run with `python test_parser.py`)

### Configuration
- **`requirements.txt`** - Python dependencies (veryfi, python-dotenv)
- **`.env.example`** - Template for API credentials (copy to `.env`)
- **`.gitignore`** - Excludes `.env` and Python cache files

### Documentation
- **`README.md`** - Complete setup and usage guide (start here!)
- **`Architecture Doc`** - Future mobile app concept (not implemented yet)

## What Gets Extracted?

The parser extracts these mortgage fields:
- ✅ Loan amounts (original & outstanding balance)
- ✅ APR (Annual Percentage Rate)
- ✅ Loan terms (e.g., "30 year fixed")
- ✅ Property address
- ✅ Payment amounts
- ✅ Lender name
- ✅ Important dates (statement, due, payment)
- ✅ Confidence scores

## Technology Stack

- **Language:** Python 3.7+
- **OCR Service:** Veryfi API (cloud-based)
- **Key Libraries:**
  - `veryfi` - SDK for document processing
  - `python-dotenv` - Environment configuration
  - Standard library: `argparse`, `json`, `re`

## Project Status

**Current State:** ✅ Working Python CLI tool
- Parses local files and URLs
- Extracts mortgage-specific fields
- Outputs formatted text or JSON
- Includes unit tests

**Future Vision:** 📱 React Native mobile app (see Architecture Doc)
- Native camera scanning
- Real-time OCR
- Editable form UI
- Offline capabilities

## Common Use Cases

1. **Batch Processing**: Parse multiple mortgage statements programmatically
2. **Data Entry Automation**: Extract data for financial systems
3. **Document Analysis**: Analyze mortgage terms and conditions
4. **API Integration**: Embed in existing Python applications
5. **Proof of Concept**: Validate OCR accuracy for mortgage documents

## Getting Help

- **Setup Issues:** See README.md "Troubleshooting" section
- **API Errors:** Check Veryfi dashboard at https://hub.veryfi.com/
- **Code Examples:** Review `example_usage.py`
- **Testing:** Run `python test_parser.py` to verify installation

## Security Notes

- ✅ API credentials stored in `.env` (git-ignored)
- ✅ HTTPS/TLS for all API communication
- ✅ No permanent document storage
- ⚠️ Keep `.env` file secure and never commit it

## Quick Start (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up credentials
cp .env.example .env
# Edit .env with your Veryfi API credentials

# 3. Process a document
python app.py your_mortgage_statement.pdf
```

## Architecture Overview

```
┌─────────────────┐
│ Mortgage Doc    │
│ (PDF/Image)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   app.py        │ ◄── Command-line interface
│   (CLI)         │     (handles args, files)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ mortgage_parser │ ◄── Extraction logic
│    .py          │     (field parsers)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Veryfi API     │ ◄── Cloud OCR service
│  (Cloud)        │     (AI processing)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Structured JSON │ ◄── Output
│ + Text Summary  │     (loan data)
└─────────────────┘
```

## File Size & Complexity

| File | Lines | Purpose | Complexity |
|------|-------|---------|------------|
| `app.py` | ~134 | CLI interface | Low |
| `mortgage_parser.py` | ~293 | Core logic | Medium |
| `example_usage.py` | ~165 | Examples | Low |
| `test_parser.py` | ~243 | Tests | Low |
| **Total** | **~835** | **Complete** | **Low-Med** |

## Dependencies

Only 2 external packages required:
1. **veryfi** (≥3.3.0) - ~30KB - OCR API client
2. **python-dotenv** (≥1.0.0) - ~21KB - Config loader

Both are lightweight and well-maintained.

## License & Contributing

This is a proof-of-concept project. Check with the repository owner for licensing and contribution guidelines.

---

**For detailed instructions, see [README.md](README.md)**
