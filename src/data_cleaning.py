import re
import pandas as pd
from datetime import datetime

def clean_and_format_data(df):
    """
    Cleans raw extracted data, identifies columns,
    and normalizes date/amounts. Returns a standardized DataFrame.
    """
    # Use first row as header
    header = df.iloc[0].values.tolist()
    df.columns = header
    df = df.iloc[1:].reset_index(drop=True)
    
    # Detect which columns are date, description, debit, credit, balance
    date_col, desc_col, debit_col, credit_col, balance_col = detect_columns(df)
    
    # If single "Amount" column, create separate debit/credit columns
    if 'Amount' in df.columns:
        if not debit_col:
            debit_col = 'debit'
            df[debit_col] = 0.0
        if not credit_col:
            credit_col = 'credit'
            df[credit_col] = 0.0
        
        for i in range(len(df)):
            val_str = df.loc[i, 'Amount']
            val = parse_amount(val_str)
            if val < 0:
                df.at[i, debit_col] = abs(val)
                df.at[i, credit_col] = 0.0
            else:
                df.at[i, credit_col] = val
                df.at[i, debit_col] = 0.0
    
    # Convert date strings to datetime
    if date_col and date_col in df.columns:
        df[date_col] = df[date_col].apply(lambda x: parse_date(str(x)))
    
    # Convert debit/credit/balance to numeric
    if debit_col and debit_col in df.columns:
        df[debit_col] = df[debit_col].apply(lambda x: parse_amount(str(x)))
    if credit_col and credit_col in df.columns:
        df[credit_col] = df[credit_col].apply(lambda x: parse_amount(str(x)))
    if balance_col and balance_col in df.columns:
        df[balance_col] = df[balance_col].apply(lambda x: parse_amount(str(x)))
    
    # Drop invalid rows
    if date_col in df.columns:
        df.dropna(subset=[date_col], inplace=True)
    
    # Rename to a standard schema
    df = df.rename(columns={
        date_col: 'date',
        desc_col: 'description',
        debit_col: 'debit',
        credit_col: 'credit',
        balance_col: 'balance'
    })
    
    # Reorder
    cols = [c for c in ['date', 'description', 'debit', 'credit', 'balance'] if c in df.columns]
    df = df[cols].reset_index(drop=True)
    
    return df

def detect_columns(df):
    """
    Attempts to detect columns for date, description, debit, credit, balance.
    """
    date_col = None
    desc_col = None
    debit_col = None
    credit_col = None
    balance_col = None
    
    for col in df.columns:
        lc = col.lower()
        if 'date' in lc:
            date_col = col
        elif 'desc' in lc or 'narration' in lc:
            desc_col = col
        elif 'debit' in lc:
            debit_col = col
        elif 'credit' in lc:
            credit_col = col
        elif 'bal' in lc:
            balance_col = col
        elif 'amount' in lc:
            # We'll handle single amount column separately
            pass
    
    return date_col, desc_col, debit_col, credit_col, balance_col

def parse_date(date_str):
    """
    Attempts to parse various date formats to a datetime object.
    """
    for fmt in ('%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return None

def parse_amount(amount_str):
    """
    Parse a currency string into a float, removing commas,
    parentheses, and other symbols.
    """
    if not amount_str or amount_str.strip() == '':
        return 0.0
    clean_str = re.sub(r'[^0-9.\-()]', '', amount_str)
    if '(' in clean_str and ')' in clean_str:
        clean_str = '-' + clean_str.replace('(', '').replace(')', '')
    try:
        return float(clean_str)
    except ValueError:
        return 0.0
