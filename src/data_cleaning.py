import openai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/ronikriger/Desktop/bank-statement-analyzer/.env")

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key


def analyze_with_chatgpt(text_files):
    """
    Sends extracted text files to ChatGPT for analysis.

    Args:
        text_files (list): List of paths to text files.

    Returns:
        list: List of analysis results from ChatGPT.
    """
    insights = []

    for file_path in text_files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        try:
            # Send the text to ChatGPT using the updated API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": f"Analyze the following bank statement data:\n{text}"}
                ]
            )

            # Access the first response choice
            insight = response['choices'][0]['message']['content']
            insights.append(insight)
            print(f"Analysis for {file_path} complete.")

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            insights.append(f"Error analyzing {file_path}: {e}")

    return insights

if __name__ == "__main__":
    # Example usage
    output_dir = "extracted_texts"
    if not os.path.exists(output_dir):
        print(f"Error: The directory '{output_dir}' does not exist.")
        exit(1)

    text_files = [os.path.join(output_dir, file) for file in os.listdir(output_dir) if file.endswith(".txt")]

    if not text_files:
        print(f"Error: No .txt files found in '{output_dir}' for analysis.")
        exit(1)

    try:
        print("Analyzing extracted text files with ChatGPT...")
        results = analyze_with_chatgpt(text_files)
        for result in results:
            print("\n--- ChatGPT Analysis ---")
            print(result)
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
