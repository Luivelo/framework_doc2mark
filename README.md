# Document to Markdown Framework

This tool processes PDF documents using Landing AI's API to extract and analyze content.

## Features

- Extract text from PDF documents using PyPDF
- Process PDFs with Landing AI's document analysis API
- Command-line interface for easy usage
- Support for processing specific pages in PDF documents

## Installation

### Prerequisites

- Python 3.13+
- Pipenv (for dependency management)

### Setup

1. Clone the repository
2. Install dependencies:

```bash
pipenv install
```

3. Create a `.env` file with your Landing AI credentials:

```
LANDING_AI_API_KEY="your_api_key_here"
LANDING_AI_URL="https://api.va.landing.ai/v1/tools/agentic-document-analysis"
```

## Usage

Run the tool with default settings (processes the first page of the default PDF):

```bash
python main.py
```

Specify a different PDF file:

```bash
python main.py --pdf path/to/your/document.pdf
```

Process a specific page (0-indexed):

```bash
python main.py --page 2
```

Combine options:

```bash
python main.py --pdf path/to/your/document.pdf --page 5
```

## Project Structure

- `main.py`: Main application script
- `docs/`: Directory containing sample PDF documents
- `.env`: Environment variables for API configuration

## Dependencies

- langchain ecosystem: For AI processing capabilities
- pypdf: For PDF text extraction
- requests: For API communication
- python-dotenv: For environment variable management
- streamlit: For web interface (future development)

## License

This project is proprietary and confidential.