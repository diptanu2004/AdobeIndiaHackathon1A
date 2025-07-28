# Adobe Hackathon Round 1A: PDF Outline Extractor

## Overview

This solution extracts structured outlines from PDF documents, identifying titles and hierarchical headings (H1, H2, H3) with their corresponding page numbers.

## Features

- **Title Extraction**: Automatically identifies document titles using font size analysis
- **Heading Detection**: Recognizes various heading patterns including:
  - Numbered sections (1., 1.1, 1.1.1)
  - Markdown-style headings (#, ##, ###)
  - All-caps headings
- **False Positive Filtering**: Excludes common non-heading text like emails, URLs, figures
- **JSON Output**: Generates clean, structured output in the required format

## Project Structure

```
/
├── extract_outline.py      # Main PDF processing logic
├── process_pdfs.py        # Docker container entry point
├── Dockerfile             # Container configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Usage

### Docker Deployment (Recommended)

```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .

# Run the container
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Process a single PDF
python extract_outline.py input.pdf -o output.json

# Process all PDFs in a directory
python process_pdfs.py
```

## Input/Output Format

### Input
- PDF files (up to 50 pages each)
- Placed in `/app/input/` directory for Docker

### Output
JSON format for each PDF:
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## Algorithm Details

### Title Extraction
- Analyzes font sizes across the first page
- Selects text with the largest font size as the title
- Cleans and normalizes the title text

### Heading Detection
Uses multiple pattern-matching approaches:

1. **Numbered Patterns**:
   - `^\d+\.\s+` for H1 (e.g., "1. Introduction")
   - `^\d+\.\d+\s+` for H2 (e.g., "1.1 Overview")
   - `^\d+\.\d+\.\d+\s+` for H3 (e.g., "1.1.1 Details")

2. **Markdown Patterns**:
   - `^#\s+` for H1
   - `^##\s+` for H2
   - `^###\s+` for H3

3. **Uppercase Fallback**:
   - Short all-caps lines classified as H3

### False Positive Filtering
Excludes lines containing:
- Email addresses and URLs
- Figure/table references
- Publication metadata (DOI, ISSN, etc.)
- Common document artifacts

## Performance Characteristics

- **Execution Time**: ≤10 seconds for 50-page PDFs
- **Model Size**: No external models (pure rule-based)
- **Architecture**: AMD64 compatible
- **Dependencies**: Minimal (only pdfplumber)

## Technical Implementation

### Core Components

1. **PDFOutlineExtractor Class**: Main processing logic
2. **Pattern Matching**: Regex-based heading detection
3. **Text Cleaning**: Removes markers and formatting artifacts
4. **JSON Serialization**: Structured output generation

### Dependencies

- **pdfplumber**: PDF text extraction and analysis
- **Python 3.9**: Core runtime environment
- **Standard Library**: re, json, os for text processing

## Error Handling

- Graceful handling of corrupted or unreadable PDFs
- Fallback title extraction when font analysis fails  
- Robust text processing for various PDF formats
- Informative error messages and logging

## Testing

The solution has been tested with:
- Academic papers with numbered sections
- Technical documents with various heading styles
- Multi-language documents (basic support)
- Documents with complex layouts

## Compliance

- ✅ AMD64 Docker compatibility
- ✅ No network dependencies (offline operation)
- ✅ Processing time under 10 seconds per 50-page PDF
- ✅ No GPU requirements
- ✅ Required JSON output format

## Build Instructions

```bash
# Clone your repository
git clone <your-repo-url>
cd <your-repo-name>

# Build Docker image
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .

# Test with sample data
docker run --rm \
  -v $(pwd)/test_input:/app/input \
  -v $(pwd)/test_output:/app/output \
  --network none \
  mysolutionname:somerandomidentifier
```

## Notes

- Keep your Git repository private until the competition deadline
- Test with diverse PDF formats to ensure robustness
- The solution prioritizes accuracy and speed within the given constraints
- No hardcoded logic - works generically across different document types