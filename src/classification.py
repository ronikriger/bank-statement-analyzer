def classify_transactions(df):
    """
    Classify each transaction into broad categories using keyword matching.
    Adds a 'category' column to the DataFrame.
    """
    categories = {
        'rent': ['rent', 'lease'],
        'utilities': ['electric', 'utility', 'water', 'gas', 'wifi', 'internet'],
        'payroll': ['payroll', 'salary', 'wages', 'paycheck'],
        'loan': ['loan', 'mortgage', 'interest', 'repayment'],
        'insurance': ['insurance', 'premium']
    }
    
    cat_list = []
    for _, row in df.iterrows():
        desc = str(row['description']).lower()
        assigned_category = 'misc'
        for cat, keywords in categories.items():
            if any(kw in desc for kw in keywords):
                assigned_category = cat
                break
        cat_list.append(assigned_category)
    
    df['category'] = cat_list
    return df
