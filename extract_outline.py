import re
import json
import os  # Added this missing import
import pdfplumber
from typing import List, Dict, Optional

class PDFOutlineExtractor:
    def __init__(self):
        # Compile regex patterns for heading detection
        self.h1_pattern = re.compile(r'^#\s+(.+)$')  # Markdown-style H1
        self.h2_pattern = re.compile(r'^##\s+(.+)$')  # Markdown-style H2
        self.h3_pattern = re.compile(r'^###\s+(.+)$')  # Markdown-style H3
        self.numbered_h1_pattern = re.compile(r'^\d+\.\s+[A-Z][A-Z\s]+$')  # "1. INTRODUCTION"
        self.numbered_h2_pattern = re.compile(r'^\d+\.\d+\s+[A-Za-z][A-Za-z\s]+$')  # "2.1 Methodology"
        
        # Common false positives to exclude
        self.exclude_patterns = [
            r'email', r'@', r'http', r'https', r'doi\.org', 
            r'figure', r'table', r'vol\.', r'pp\.', r'no\.',
            r'received|revised|accepted', r'issn', r'copyright',
            r'prepared by', r'date:', r'keywords:'
        ]

    def extract_outline(self, pdf_path: str) -> Dict:
        """
        Extract a structured outline from a PDF document with proper H1-H3 hierarchy
        """
        outline = []
        title = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            # Extract title from first page
            if len(pdf.pages) > 0:
                title = self._extract_title(pdf.pages[0])
            
            # Process each page for headings
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue
                
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Check if line matches any heading pattern
                    heading_level = self._detect_heading_level(line)
                    if heading_level:
                        outline.append({
                            "level": heading_level,
                            "text": self._clean_heading_text(line),
                            "page": page_num
                        })
        
        return {
            "title": title if title else os.path.splitext(os.path.basename(pdf_path))[0],
            "outline": outline
        }

    def _extract_title(self, page) -> str:
        """
        Extract title from page's largest text element
        """
        words = page.extract_words(extra_attrs=["size"])
        if not words:
            return ""
        
        # Find text with largest font size (likely title)
        max_size = max(word["size"] for word in words)
        title_words = [word["text"] for word in words if abs(word["size"] - max_size) < 0.5]
        
        # Join and clean title text
        title = " ".join(title_words)
        title = re.sub(r'\s+', ' ', title).strip()
        return title

    def _detect_heading_level(self, text: str) -> Optional[str]:
        """
        Detect heading level (H1-H3) based on text patterns and styling
        """
        # Skip common false positives
        if any(re.search(pattern, text.lower()) for pattern in self.exclude_patterns):
            return None

        text = text.strip()

        # Match numbered headings
        if re.match(r'^\d+\.\d+\.\d+\s+', text):
            return "H3"
        elif re.match(r'^\d+\.\d+\s+', text):
            return "H2"
        elif re.match(r'^\d+\.\s+', text):
            return "H1"

        # Match Markdown-style
        if self.h1_pattern.match(text):
            return "H1"
        if self.h2_pattern.match(text):
            return "H2"
        if self.h3_pattern.match(text):
            return "H3"

        # All uppercase short lines as fallback H3
        if text.isupper() and 2 <= len(text.split()) <= 8 and len(text) < 80:
            return "H3"

        return None

    def _clean_heading_text(self, text: str) -> str:
        """
        Clean heading text by removing markers and extra spaces
        """
        # Remove markdown-style markers
        text = re.sub(r'^#+\s+', '', text)
        
        # Remove page numbers and dots (e.g., "1. INTRODUCTION ...... 3")
        text = re.sub(r'\s*\.+\s*\d+\s*$', '', text)
        
        return text.strip()

    def process_pdf(self, input_pdf: str, output_json: str = None):
        """
        Process a single PDF and save outline to JSON
        """
        if not output_json:
            output_json = os.path.splitext(input_pdf)[0] + "_outline.json"
        
        try:
            outline = self.extract_outline(input_pdf)
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(outline, f, indent=2, ensure_ascii=False)
            print(f"Successfully processed {input_pdf} -> {output_json}")
            return True
        except Exception as e:
            print(f"Error processing {input_pdf}: {str(e)}")
            return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PDF Outline Extractor")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output JSON file path (optional)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} does not exist")
        exit(1)
    
    extractor = PDFOutlineExtractor()
    extractor.process_pdf(args.input, args.output)