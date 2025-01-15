import camelot
import pandas as pd

def extract_data_from_pdf(pdf_path):
    """
    Uses Camelot to read tables from a PDF.
    Returns a combined Pandas DataFrame of all pages/tables.
    """
    # Try 'lattice' or 'stream' depending on your PDF layout
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
    
    df_list = [table.df for table in tables]
    
    if df_list:
        full_df = pd.concat(df_list, ignore_index=True)
    else:
        full_df = pd.DataFrame()
    
    return full_df
