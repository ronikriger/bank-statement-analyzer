# File: pdf_pipeline.py

import os
from src.extract_bank_data import extract_text_from_pdf
from src.data_cleaning import analyze_with_chatgpt

def main():
    # ---------------------------
    # Directories
    # ---------------------------
    pdf_dir = "bankstatements"
    output_dir = "extracted_texts"
    os.makedirs(output_dir, exist_ok=True)

    # ---------------------------
    # Step 1: Process Each PDF – Extract Text and Analyze with ChatGPT
    # ---------------------------
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            print(f"\nProcessing {pdf_file}...")

            # Extract text from the PDF; each page's text is saved as a separate .txt file
            try:
                print("Extracting text from PDF...")
                text_files = extract_text_from_pdf(pdf_path, output_dir)
                print(f"Text extraction complete for {pdf_file}.")
            except Exception as e:
                print(f"Error extracting text from {pdf_file}: {e}")
                continue

            # Analyze the extracted text with ChatGPT
            try:
                print("Analyzing extracted text with ChatGPT...")
                insights = analyze_with_chatgpt(text_files)
                print(f"\n--- ChatGPT Analysis for {pdf_file} ---")
                for insight in insights:
                    print(insight)
            except Exception as e:
                print(f"Error analyzing {pdf_file} with ChatGPT: {e}")

    # ---------------------------
    # Step 2: ML-Driven Transaction Analysis
    # ---------------------------
    try:
        from src.transaction_analysis import ml_transaction_insights
        # List all .txt files in the extracted texts directory
        all_text_files = [
            os.path.join(output_dir, file)
            for file in os.listdir(output_dir)
            if file.endswith(".txt")
        ]
        if all_text_files:
            print("\nPerforming ML-driven transaction analysis on all extracted text files...")
            ml_summary = ml_transaction_insights(all_text_files, contamination=0.05)
            print("\n--- ML Transaction Insights ---")
            print(ml_summary)
        else:
            print("No extracted text files available for ML-driven transaction analysis.")
    except Exception as e:
        print(f"Error during ML transaction analysis: {e}")

    # ---------------------------
    # Step 3: Time Series Forecasting – Predict Future Cash Flow
    # ---------------------------
    try:
        from src.transaction_analysis import load_transactions_from_text_files, apply_categorization
        from src.forecasting import forecast_cash_flow

        # Reload transactions from the extracted text files
        all_text_files = [
            os.path.join(output_dir, file)
            for file in os.listdir(output_dir)
            if file.endswith(".txt")
        ]
        if not all_text_files:
            print("No extracted text files available for forecasting.")
        else:
            # Load transactions into a DataFrame
            df = load_transactions_from_text_files(all_text_files)
            if df.empty:
                print("No transactions parsed from the provided text files for forecasting.")
            else:
                # Apply basic categorization (ensuring the DataFrame contains the required columns)
                df = apply_categorization(df)
                # Forecast future cash flow (e.g., forecast next 30 days)
                forecast, forecast_plot = forecast_cash_flow(df, forecast_period=30, output_dir=output_dir)
                print("\n--- Time Series Forecasting ---")
                print("Forecasted Cash Flow for the next 30 days:")
                print(forecast)
                print("Forecast plot saved to:", forecast_plot)
    except Exception as e:
        print(f"Error during time series forecasting: {e}")

if __name__ == "__main__":
    main()
