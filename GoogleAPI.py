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
    client = genai.Client(api_key=GEMINI_API_KEY)

    uncategorized = df[df['Category'] == 'Uncategorized']

    if uncategorized.empty:
        return df

    print("Categorizing expenses...")

    descriptions = uncategorized['Description'].tolist()
    indices      = uncategorized.index.tolist()

    numbered = "\n".join(f"{i+1}. {desc}" for i, desc in enumerate(descriptions))

    prompt = (
        "Categorize each transaction below into exactly one of these categories: "
        "Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Personal, "
        "Debt, Savings, Gifts/Donations, Entertainment, Miscellaneous, Transfer, Bills, Education.\n"
        "Reply with one category per line, in the same order, no extra text.\n\n"
        f"{numbered}"
    )

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    categories = [line.strip() for line in response.text.strip().splitlines() if line.strip()]

    for i, index in enumerate(indices):
        if i < len(categories):
            df.at[index, 'Category'] = categories[i]
            print(f"{df.at[index, 'Description']} → {categories[i]}")

    return df


def ask_finance_question(question, df):
    client = genai.Client(api_key=GEMINI_API_KEY)

    total_income = df[df['Amount'] > 0]['Amount'].sum()
    total_spent  = df[df['Amount'] < 0]['Amount'].sum()
    net          = total_income + total_spent
    by_category  = (
        df[df['Amount'] < 0]
        .groupby('Category')['Amount']
        .sum().abs()
        .sort_values(ascending=False)
        .to_dict()
    )
    category_lines = "\n".join(f"  - {k}: ${v:,.2f}" for k, v in by_category.items())

    context = (
        f"Total Income: ${total_income:,.2f}\n"
        f"Total Spent: ${abs(total_spent):,.2f}\n"
        f"Net Balance: ${net:,.2f}\n"
        f"Spending by category:\n{category_lines}"
    )

    prompt = (
        "You are a concise personal finance advisor. "
        "Answer the question using the user's real financial data below. "
        "Format your response with a short summary, clear section titles, and bullet points. "
        "Remove wordiness — be direct and actionable.\n\n"
        f"Financial data:\n{context}\n\n"
        f"Question: {question}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

