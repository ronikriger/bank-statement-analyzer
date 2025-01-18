import pdfplumber
import os

def extract_text_from_pdf(pdf_path, output_dir):
    """
    Extracts raw text from a PDF file and saves it to a .txt file.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save the extracted text files.

    Returns:
        list: List of file paths to the saved text files.
    """
    extracted_files = []

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract raw text from the page
            text = page.extract_text()

            # Save the extracted text to a file
            output_file = os.path.join(output_dir, f"page_{page_num + 1}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)

            extracted_files.append(output_file)
            print(f"Page {page_num + 1} text saved to {output_file}")

    return extracted_files

if __name__ == "__main__":
    # Example usage
    pdf_path = input("Enter the PDF file path: ")
    output_dir = "extracted_texts"

    try:
        print("Extracting text from PDF...")
        files = extract_text_from_pdf(pdf_path, output_dir)
        print(f"Text extraction complete. Files saved in: {output_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")
