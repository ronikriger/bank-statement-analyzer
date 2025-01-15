import sys
import pandas as pd

from src.data_extraction import extract_data_from_pdf
from src.data_cleaning import clean_and_format_data
from src.classification import classify_transactions
from src.analytics import analyze_finances
from src.reporting import generate_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_pipeline.py <path_to_pdf_statement>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    print(f"Processing PDF: {pdf_path}")
    
    # 1. Extract data
    raw_df = extract_data_from_pdf(pdf_path)
    if raw_df.empty:
        print("No tables found or PDF parsing failed.")
        sys.exit(0)
    
    # 2. Clean & Normalize
    cleaned_df = clean_and_format_data(raw_df)
    
    # 3. Classify Transactions
    classified_df = classify_transactions(cleaned_df)
    
    # 4. Analyze
    analysis_results = analyze_finances(classified_df)
    
    # 5. Generate Report
    generate_report(classified_df, analysis_results)

if __name__ == "__main__":
    main()
