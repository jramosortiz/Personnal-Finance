import google.generativeai as genai
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
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

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
        response = model.generate_content(
            f"Categorize: {row['Description']} into  Housing,Transportation,Food,Utilities,Insurance,Medical/Healthcare,Personal,"
            f"Debt,Savings,Gifts/Donations,Entertainment,Miscellaneous,Transportation, Transfer, Bills, Education"
            f"only give me the answer no need for explanation.",)
        #Replace it with the new category
        df.at[index,'Category'] = response.text
        print("Change:")
        print(f"Description: {row['Description']}")
        print(f"Current Category: {df.at[index,'Category']}")

    return df

def AI_Agent(request):
    # Suppress unnecessary Google SDK warnings
    logging.getLogger('google').setLevel(logging.WARNING)
    logging.getLogger('absl').setLevel(logging.ERROR)

    # Configure Gemini API
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(request + "make sure is simple anought ")

    print(response.text)


AI_Agent('Help get into my goal by the end of the year. My goal is to save 5000 dollards. I get pay every 2 weeks for example I get payed today around 1230 $.')