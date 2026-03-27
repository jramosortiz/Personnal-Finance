from google import genai
import logging
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Suppress unnecessary Google SDK warnings
logging.getLogger('google').setLevel(logging.WARNING)
logging.getLogger('absl').setLevel(logging.ERROR)

def categorize_expense(df):
    # Suppress unnecessary Google SDK warnings
    logging.getLogger('google').setLevel(logging.WARNING)
    logging.getLogger('absl').setLevel(logging.ERROR)

    # Configure Gemini API
    client = genai.Client(api_key=GEMINI_API_KEY)

    uncategorized = df[df['Category'] == 'Uncategorized'][['Description', 'Category']]

    #if empty return
    if uncategorized.empty:
        return df

    print("Categorizing expenses...")
    # Iterate through uncategorized transactions
    for index, row in uncategorized.iterrows():
        print(f"\nTransaction {index}:")
        print(f"Description: {row['Description']}")
        print(f"Current Category: {row['Category']}")
        #Send API CALL and Receive the Results
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Categorize: {row['Description']} into  Housing,Transportation,Food,Utilities,Insurance,Medical/Healthcare,Personal,"
            f"Debt,Savings,Gifts/Donations,Entertainment,Miscellaneous,Transportation, Transfer, Bills, Education"
            f"only give me the answer no need for explanation.",)
        #Replace it with the new category
        df.at[index,'Category'] = response.text
        print("Change:")
        print(f"Description: {row['Description']}")
        print(f"Current Category: {df.at[index,'Category']}")



    return df

