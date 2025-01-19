# File: dashboard.py

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Import functions from transaction_analysis for data loading and processing.
from src.transaction_analysis import (
    load_transactions_from_text_files,
    apply_categorization,
    detect_anomalies
)

# Directory where extracted text files are stored.
EXTRACTED_TEXT_DIR = "extracted_texts"

@st.cache_data
def load_and_process_data():
    """
    Loads transactions from extracted text files, applies categorization and anomaly detection,
    and returns a processed DataFrame.
    """
    # List all .txt files in the output directory
    text_files = [
        os.path.join(EXTRACTED_TEXT_DIR, file)
        for file in os.listdir(EXTRACTED_TEXT_DIR)
        if file.endswith(".txt")
    ]
    
    # Load transactions from all text files
    df = load_transactions_from_text_files(text_files)
    
    if df.empty:
        st.error("No transactions found in the extracted texts!")
        return pd.DataFrame()
    
    # Apply categorization and anomaly detection
    df = apply_categorization(df)
    df = detect_anomalies(df, contamination=0.05)
    
    # Ensure that dates are proper datetime objects and drop rows without dates.
    df = df[df["date"].notna()]
    df["date"] = pd.to_datetime(df["date"])
    
    return df

def main():
    st.title("Bank Statement Transaction Analysis Dashboard")
    st.markdown(
        """
        This interactive dashboard allows you to explore the extracted transaction data from the bank statements.
        Use the filters in the sidebar to drill down into specific insights based on transaction category, date range,
        or anomaly status.
        """
    )
    
    # Load and process transaction data
    df = load_and_process_data()
    if df.empty:
        st.stop()
    
    # ----------------------------
    # Sidebar Filters
    # ----------------------------
    st.sidebar.header("Filters")
    
    # Filter by Category
    categories = df["category"].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Select Transaction Categories",
        options=categories,
        default=categories
    )
    
    # Filter by Date Range
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    
    # Filter to show only anomalies if desired
    show_anomalies = st.sidebar.checkbox("Show only anomalies", value=False)
    
    # Apply Filters to the DataFrame
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]
    
    if isinstance(date_range, list) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date) &
            (filtered_df["date"].dt.date <= end_date)
        ]
    
    if show_anomalies:
        filtered_df = filtered_df[filtered_df["anomaly"] == -1]
    
    st.subheader("Filtered Transaction Data")
    st.write(filtered_df.sort_values("date", ascending=False))
    
    # ----------------------------
    # Visualizations
    # ----------------------------
    
    # Scatter Plot: Transaction Amounts Over Time
    st.subheader("Transaction Amounts Over Time")
    if not filtered_df.empty:
        fig_time = px.scatter(
            filtered_df,
            x="date",
            y="amount",
            color="category",
            symbol=filtered_df["anomaly"].apply(lambda x: "Anomaly" if x == -1 else "Normal"),
            hover_data=["description"],
            title="Transaction Amounts Over Time"
        )
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")
    
    # Bar Chart: Transaction Count by Category
    st.subheader("Transaction Count by Category")
    if not filtered_df.empty:
        # Compute category counts and rename the columns appropriately.
        cat_counts = filtered_df["category"].value_counts().reset_index()
        cat_counts.columns = ["category", "count"]
        fig_bar = px.bar(
            cat_counts,
            x="category",
            y="count",
            labels={"category": "Category", "count": "Count"},
            title="Transactions per Category"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No data available to display category counts.")
    
    # Summary Information
    st.subheader("Summary Insights")
    st.markdown(f"**Total Transactions**: {len(filtered_df)}")
    anomaly_count = (filtered_df["anomaly"] == -1).sum()
    st.markdown(f"**Detected Anomalies**: {anomaly_count}")

if __name__ == "__main__":
    main()
