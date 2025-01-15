def generate_report(df, analysis):
    """
    Print a simple textual report based on the analysis dictionary.
    """
    monthly_summary = analysis['monthly_summary']
    recurring_expenses = analysis['recurring_expenses']
    existing_loan = analysis['existing_loan']
    
    print("=== Financial Analysis Report ===\n")
    
    print(">> Monthly Inflow/Outflow:")
    for _, row in monthly_summary.iterrows():
        print(f"   Period: {row['year_month']}")
        print(f"     Total Debit (Outflow):  {row['debit']:.2f}")
        print(f"     Total Credit (Inflow):  {row['credit']:.2f}")
        print(f"     Net Cash Flow:          {row['net_flow']:.2f}\n")
    
    print(">> Recurring Expenses Detected:")
    if recurring_expenses:
        for item in recurring_expenses:
            print(f"   Description: {item['description']}, Category: {item['category']} (appears multiple months)")
    else:
        print("   No recurring expenses detected (or insufficient data)")
    print()
    
    print(">> Existing Loan Check:")
    if existing_loan:
        print("   Potential existing loan found (loan or interest payments detected).")
    else:
        print("   No clear indication of existing loan in transactions.")
    print()
    
    # Basic recommendation logic
    positive_months = monthly_summary[monthly_summary['net_flow'] > 0].shape[0]
    total_months = monthly_summary.shape[0]
    
    if total_months > 0 and (positive_months / total_months) > 0.7:
        print(">> Recommendation: Likely a good candidate for a business loan.")
    else:
        print(">> Recommendation: Further review needed (cash flow not consistently positive).")
    
    print("\n=================================\n")
