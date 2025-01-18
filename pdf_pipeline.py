import os
from src.extract_bank_data import extract_text_from_pdf
from src.data_cleaning import analyze_with_chatgpt

def main():
    # Directory containing your PDFs
    pdf_dir = "bankstatements"
    output_dir = "extracted_texts"
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each PDF
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            print(f"Processing {pdf_file}...")

            # Step 1: Extract text from PDF
            try:
                print("Extracting text...")
                text_files = extract_text_from_pdf(pdf_path, output_dir)
                print(f"Text extraction complete for {pdf_file}.")
            except Exception as e:
                print(f"Error extracting text from {pdf_file}: {e}")
                continue

            # Step 2: Analyze text with ChatGPT
            try:
                print("Analyzing extracted text with ChatGPT...")
                insights = analyze_with_chatgpt(text_files)
                print(f"\n--- Analysis for {pdf_file} ---")
                for insight in insights:
                    print(insight)
            except Exception as e:
                print(f"Error analyzing {pdf_file}: {e}")

if __name__ == "__main__":
    main()
