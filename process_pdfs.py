#!/usr/bin/env python3
"""
Process all PDFs from input directory and generate JSON outlines in output directory
This script is designed to work with the Docker container setup for Round 1A
"""

import os
import glob
from extract_outline import PDFOutlineExtractor

def main():
    """
    Process all PDFs from /app/input and save results to /app/output
    """
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files in input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Initialize the extractor
    extractor = PDFOutlineExtractor()
    
    # Process each PDF
    success_count = 0
    for pdf_file in pdf_files:
        try:
            # Get the base filename without extension
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            
            # Create output JSON filename
            output_json = os.path.join(output_dir, f"{base_name}.json")
            
            print(f"Processing: {pdf_file}")
            
            # Process the PDF
            if extractor.process_pdf(pdf_file, output_json):
                success_count += 1
                print(f"✓ Successfully processed: {base_name}.pdf -> {base_name}.json")
            else:
                print(f"✗ Failed to process: {base_name}.pdf")
                
        except Exception as e:
            print(f"✗ Error processing {pdf_file}: {str(e)}")
    
    print(f"\nProcessing complete: {success_count}/{len(pdf_files)} files processed successfully")

if __name__ == "__main__":
    main()