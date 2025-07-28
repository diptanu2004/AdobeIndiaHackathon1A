FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main script
COPY extract_outline.py .
COPY process_pdfs.py .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set executable permissions
RUN chmod +x process_pdfs.py

# Default command to process all PDFs in input directory
CMD ["python", "process_pdfs.py"]