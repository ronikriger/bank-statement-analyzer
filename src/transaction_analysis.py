# File: src/transaction_analysis.py

import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

def parse_transactions_from_text(text):
    """
    Extracts structured transactions from a block of text.
    
    Two methods are attempted:
    
    1. Primary Pattern (expects a full date: MM/DD/YYYY, description, and amount):
         Example match: "12/31/2017 Some transaction description 1,234.56"
    
    2. Secondary Pattern (line-by-line, for shorter date formats):
         Example line: "01 Dec Account Fee 4.00 $804.80 CR"
         In this case, we extract the date (without year), description, and two amounts
         (assuming the first amount is the debit and the second is the credit). We then
         set the transaction amount to -debit if present, else +credit.
    
    Returns:
        List of dictionaries, each containing 'date', 'description', and 'amount'.
    """
    transactions = []
    
    # Debug: Print a snippet of the text being processed.
    print("DEBUG: Extracted text snippet:", text[:200])
    
    # ----------------------------
    # Primary Pattern: Full Date Format
    # ----------------------------
    # This pattern expects:
    # - a date in MM/DD/YYYY format,
    # - a description (letters, numbers, spaces, hyphens, periods, commas, ampersand),
    # - an optional dollar sign, followed by a numeric amount (with commas/decimals).
    primary_pattern = re.compile(
        r'(\d{2}/\d{2}/\d{4})\s+([A-Za-z0-9 \-.,&]+?)\s+\$?([\d,]+\.\d{2})'
    )
    
    matches = primary_pattern.findall(text)
    print("DEBUG: Primary regex matches found:", matches)
    
    if matches:
        for match in matches:
            date_str, description, amount_str = match
            
            # Convert date string to datetime object
            try:
                date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            except Exception as e:
                print(f"DEBUG: Could not parse date '{date_str}': {e}")
                date_obj = None
            
            # Convert the amount string to a float (removing commas)
            try:
                amount = float(amount_str.replace(",", ""))
            except Exception as e:
                print(f"DEBUG: Could not parse amount '{amount_str}': {e}")
                amount = np.nan
            
            transactions.append({
                "date": date_obj,
                "description": description.strip(),
                "amount": amount
            })
    
    # ----------------------------
    # Secondary Pattern: Short Date Format (e.g., "01 Dec")
    # ----------------------------
    if not transactions:
        print("DEBUG: No transactions extracted using primary pattern. Trying secondary pattern...")
        
        # This regex is intended to capture lines starting with a short date format.
        # Example line: "01 Dec Account Fee 4.00 $804.80 CR"
        # Group 1: Date (e.g., "01 Dec")
        # Group 2: Description
        # Group 3: Debit (optional)
        # Group 4: Credit (optional)
        secondary_pattern = re.compile(
            r'^(\d{1,2}\s+[A-Za-z]{3})\s+([\w\s\-.,&]+?)\s+(\$?[\d,]+\.\d{2})\s+(\$?[\d,]+\.\d{2})',
            re.MULTILINE
        )
        
        sec_matches = secondary_pattern.findall(text)
        print("DEBUG: Secondary regex matches found:", sec_matches)
        
        for match in sec_matches:
            date_str, description, debit_str, credit_str = match
            # Here, we don't have the year. For demonstration, we use a default year (e.g., current year)
            try:
                date_obj = datetime.strptime(f"{date_str} {datetime.now().year}", "%d %b %Y")
            except Exception as e:
                print(f"DEBUG: Could not parse short date '{date_str}': {e}")
                date_obj = None
            
            # Determine the transaction amount:
            # If debit is non-zero, assume it's a debit (negative).
            # Otherwise, use the credit amount (positive).
            try:
                debit = float(debit_str.replace("$", "").replace(",", ""))
            except Exception as e:
                print(f"DEBUG: Could not parse debit '{debit_str}': {e}")
                debit = 0.0
            
            try:
                credit = float(credit_str.replace("$", "").replace(",", ""))
            except Exception as e:
                print(f"DEBUG: Could not parse credit '{credit_str}': {e}")
                credit = 0.0
            
            if debit > 0:
                amount = -debit
            else:
                amount = credit
            
            transactions.append({
                "date": date_obj,
                "description": description.strip(),
                "amount": amount
            })
    
    return transactions

def load_transactions_from_text_files(text_files):
    """
    Read each text file and extract transactions.
    
    Args:
        text_files (list): List of paths to text files.
        
    Returns:
        DataFrame containing all transactions.
    """
    all_transactions = []
    for file_path in text_files:
        print("DEBUG: Processing file:", file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        file_transactions = parse_transactions_from_text(text)
        print(f"DEBUG: Transactions extracted from {file_path}: {file_transactions}")
        if file_transactions:
            all_transactions.extend(file_transactions)
        else:
            print("DEBUG: No transactions extracted from", file_path)
    
    if not all_transactions:
        print("DEBUG: No transactions found in any files.")
        return pd.DataFrame()
    
    return pd.DataFrame(all_transactions)

def categorize_transaction(description):
    """
    A simple rule-based categorization based on keywords in the description.
    
    Returns:
        Category as a string.
    """
    desc = description.lower()
    if any(keyword in desc for keyword in ["deposit", "credit", "payment received", "incoming"]):
        return "Deposit"
    elif any(keyword in desc for keyword in ["withdrawal", "check", "card", "payment", "debit", "purchase"]):
        return "Expense"
    else:
        return "Other"

def apply_categorization(df):
    """
    Apply categorization to a DataFrame of transactions.
    
    Args:
        df (DataFrame): DataFrame with a 'description' column.
        
    Returns:
        DataFrame with an added 'category' column.
    """
    if "description" not in df.columns:
        raise ValueError("DataFrame must contain a 'description' column.")
    df["category"] = df["description"].apply(categorize_transaction)
    return df

def detect_anomalies(df, contamination=0.05):
    """
    Use Isolation Forest to detect anomalous transactions based on amount.
    
    Args:
        df (DataFrame): DataFrame with a numeric 'amount' column.
        contamination (float): The proportion of outliers in the data.
        
    Returns:
        DataFrame with an added 'anomaly' column (1 for normal, -1 for anomaly).
    """
    if df.empty:
        return df
    
    X = df["amount"].values.reshape(-1, 1)
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    preds = iso_forest.fit_predict(X)
    df["anomaly"] = preds  # normal: 1, anomaly: -1
    return df

def visualize_transactions(df, output_dir="extracted_texts"):
    """
    Generate and save visualizations:
    - Scatter plot of transaction amounts colored by category.
    - Highlight anomalies.
    
    Args:
        df (DataFrame): DataFrame containing transactions.
        output_dir (str): Directory to save the plot image.
        
    Returns:
        Path to the saved image.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10, 6))
    
    categories = df["category"].unique()
    colors = plt.cm.get_cmap("tab10", len(categories))
    
    for i, category in enumerate(categories):
        subset = df[df["category"] == category]
        plt.scatter(subset.index, subset["amount"], label=category,
                    color=colors(i), s=50, alpha=0.7)
    
    if "anomaly" in df.columns:
        anomalies = df[df["anomaly"] == -1]
        if not anomalies.empty:
            plt.scatter(anomalies.index, anomalies["amount"], label="Anomaly",
                        color="red", marker="x", s=100)
    
    plt.xlabel("Transaction Index")
    plt.ylabel("Amount")
    plt.title("Transaction Amounts by Category with Anomalies Highlighted")
    plt.legend()
    
    plot_file = os.path.join(output_dir, "transaction_analysis.png")
    plt.savefig(plot_file, bbox_inches="tight")
    plt.close()
    return plot_file

def ml_transaction_insights(text_files, contamination=0.05):
    """
    Process text files containing extracted bank statement data to produce ML insights.
    
    Args:
        text_files (list): List of file paths to the extracted text files.
        contamination (float): Contamination rate for anomaly detection.
    
    Returns:
        A string summary of insights along with the path to a visualization plot.
    """
    df = load_transactions_from_text_files(text_files)
    
    if df.empty:
        return "No transactions parsed from the provided text files."
    
    df = apply_categorization(df)
    df = detect_anomalies(df, contamination)
    plot_path = visualize_transactions(df)
    
    insights = []
    insights.append("=== Transaction Analysis ===")
    insights.append("Total transactions: {}".format(len(df)))
    insights.append("Transactions by category:")
    insights.append(df["category"].value_counts().to_string())
    
    anomaly_count = (df["anomaly"] == -1).sum()
    insights.append("\nDetected anomalies: {} transactions".format(anomaly_count))
    insights.append("Visualization plot saved to: {}".format(plot_path))
    
    return "\n".join(insights)

# Standalone testing when running this file directly:
if __name__ == "__main__":
    output_dir = "extracted_texts"
    text_files = [os.path.join(output_dir, file) for file in os.listdir(output_dir) if file.endswith(".txt")]
    
    if not text_files:
        print("No text files found in '{}' for ML transaction analysis.".format(output_dir))
        exit(1)
    
    summary = ml_transaction_insights(text_files, contamination=0.05)
    print(summary)
