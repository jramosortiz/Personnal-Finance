import pandas as pd
import GoogleAPI


def load_TransactionFile(csv_file):
    #Load CSV with Columns
    try:
        df = pd.read_excel(csv_file,engine='openpyxl')
        print("Loaded columns:", df.columns.tolist())
        print(df.head())
        if df.empty or not all(col in df.columns for col in ['Posting Date', 'Description', 'Amount', 'Balance']):
            raise ValueError("Invalid CSV format. Requires Posting Date, Description, Amount columns.")

        # Change variable type
        df['Posting Date'] = pd.to_datetime(df['Posting Date'], format='%m/%d/%Y', errors='coerce')
        df['Description'] = df['Description'].astype(str)
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')

        # Sort by date
        df = df.sort_values('Posting Date')

        # Add 'Category' column with improved logic
        df['Category'] = 'Uncategorized'
        # Categorize based on Description and Type
        df.loc[df['Description'].str.contains('STARBUCKS|CHIPOTLE|PUBLIX|WAWA', case=False, na=False), 'Category'] = 'Food'
        df.loc[df['Description'].str.contains('AMC', case=False, na=False), 'Category'] = 'Entertainment'
        df.loc[df['Description'].str.contains('Zelle', case=False, na=False), 'Category'] = 'Transfer'
        df.loc[df['Description'].str.contains('SHELL OIL', case=False, na=False), 'Category'] = 'Transportation'
        df.loc[df['Description'].str.contains('Payment to Chase|CAPITAL ONE|DISCOVER|BEST BUY', case=False,
                                              na=False), 'Category'] = 'Bills'
        df.loc[df['Description'].str.contains('Univ of Florida', case=False, na=False), 'Category'] = 'Education'

        # Handle refunds (positive amounts in debit-like transactions)
        df.loc[(df['Amount'] > 0) & (df['Category'] != 'Income'), 'Category'] = 'Refund'

        # Get uncategorize category assign with Gemini AI
        df = GoogleAPI.categorize_expense(df)

        print(df[['Posting Date', 'Description', 'Amount', 'Balance', 'Category']])
        return df
    except Exception as e:
        raise Exception(f"Error loading CSV: {e}")