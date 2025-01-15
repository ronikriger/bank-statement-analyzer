import pandas as pd

def analyze_finances(df):
    """
    Summarize monthly inflows/outflows, detect recurring expenses,
    and check for loan payments.
    Returns an 'analysis' dict with key metrics.
    """
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Compute monthly inflow/outflow
    monthly_summary = df.groupby('year_month').agg({
        'debit': 'sum',
        'credit': 'sum'
    }).reset_index()
    monthly_summary['net_flow'] = monthly_summary['credit'] - monthly_summary['debit']
    
    # Recurring payments
    recurring_expenses = detect_recurring_payments(df)
    
    # Check for an existing loan
    loan_payments = df[df['category'] == 'loan']
    potential_existing_loan = not loan_payments.empty
    
    analysis_results = {
        'monthly_summary': monthly_summary,
        'recurring_expenses': recurring_expenses,
        'existing_loan': potential_existing_loan
    }
    return analysis_results

def detect_recurring_payments(df):
    """
    Identify recurring payments by grouping on description/category
    and checking if they appear in multiple months.
    """
    df['year_month'] = df['date'].dt.to_period('M')
    
    group = df.groupby(['description', 'category', 'year_month']).size().reset_index(name='count')
    recurring = group.groupby(['description', 'category']).size().reset_index(name='months_count')
    recurring_items = recurring[recurring['months_count'] > 1]
    
    return recurring_items.to_dict('records')
