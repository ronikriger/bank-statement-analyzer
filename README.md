# Bank Statement Analyzer


**Bank Statement Analyzer** is a comprehensive tool designed to extract, analyze, and visualize transaction data from bank statements. Leveraging advanced machine learning techniques and an interactive dashboard, this project provides financial insights, detects anomalies, and forecasts future cash flows—helping businesses and individuals make informed decisions.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Pipeline](#running-the-pipeline)
  - [Launching the Dashboard](#launching-the-dashboard)
- [Project Structure](#project-structure)
- [Modules](#modules)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- **PDF Text Extraction**: Automatically extracts text from multi-page PDF bank statements.
- **ChatGPT Analysis**: Uses OpenAI's ChatGPT API to generate narrative insights from extracted text.
- **ML Transaction Analysis**:  
  - Parses raw text into structured transaction data.  
  - Categorizes transactions (e.g., Deposits, Expenses).  
  - Detects anomalies using machine learning (Isolation Forest).  
  - Provides detailed visualizations.
- **Time Series Forecasting**: Aggregates historical transactions to forecast future cash flows with an Exponential Smoothing model.
- **Interactive Dashboard**: A Streamlit-based interface for exploring transactions, filtering data, and viewing dynamic charts and forecasting outputs.
- **Comprehensive Reporting**: Delivers clear, actionable insights derived from bank statement data.

## Demo

<img width="1440" alt="Screenshot 2025-01-21 at 04 06 51" src="https://github.com/user-attachments/assets/c9689189-1fd4-4ab6-8561-23a55c4da9bc" />


## Installation

### Prerequisites

- **Python 3.7 or higher** is required.
- It is highly recommended to use a virtual environment.

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ronikriger/bank-statement-analyzer.git
   cd bank-statement-analyzer
   
2. **Clone the Repository**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
Make sure that requirements.txt includes all necessary packages (see Dependencies for a sample list).

## Usage

### Running the Pipeline

#### Prepare the Bank Statement PDFs

- Place your bank statement PDFs in the `bankstatements/` directory.
- Name them appropriately (e.g., `BankStatement1.pdf`, `BankStatement2.pdf`, etc.).

#### Run the Pipeline
    ```bash
    python pdf_pipeline.py
![image](https://github.com/user-attachments/assets/8c3c13e5-1554-4067-8e0c-4f6f8926c077)



#### What Happens:

- Text Extraction:
- The pipeline extracts text from each PDF, saving individual pages as .txt files in the extracted_texts/ directory.

#### ChatGPT Analysis:
- Each extracted text file is processed by ChatGPT to generate narrative insights.

#### ML Transaction Analysis:
- All text files are consolidated; transactions are parsed, categorized, and anomalies are detected.

#### Time Series Forecasting:
- Historical cash flows are aggregated on a daily basis, and an Exponential Smoothing model forecasts future cash flows (e.g., for the next 30 days).
- The forecasted results are printed, and a forecast plot is saved in the extracted_texts/ directory.

#### Launching the Dashboard:
- Ensure Streamlit and Plotly Are Installed
- If you haven't yet installed these packages, run:

    ```bash
    pip install streamlit plotly

      ```bash
    streamlit run dashboard.py

#### Dashboard Features:

## Filters:
- Choose transaction categories, set date ranges, and filter anomalies.

## Visualizations:

- A scatter plot displays transaction amounts over time (with anomaly markers).
- A bar chart summarizes transactions per category.
- Key metrics such as total transactions and detected anomalies are displayed.

## PLEASEE Install dependencies!!!! 
         ```bash
         pip install -r requirements.txt

