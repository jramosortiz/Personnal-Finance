from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd



#Create Line chart
def visualize_line(window, df):
    fig = Figure(figsize=(4, 4))
    ax = fig.add_subplot(111)

    # Filter expenses (negative amounts, exclude Transfers and Refunds)
    expenses = df[(df['Amount'] < 0) & (~df['Category'].isin(['Transfer', 'Refund']))].groupby('Category')[
        'Amount'].sum().abs()

    # Line chart for balance over time
    df['Posting Date'] = pd.to_datetime(df['Posting Date'], format='%m/%Y',errors='coerce')
    ax.plot(df['Posting Date'], df['Balance'], marker='o', color='#66b3ff')
    ax.title.set_text('Balance Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Balance')
    ax.grid(True, axis='y')

    # Embed the figure into the tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=2, padx=10, pady=10)




#Create Bar chart
def visualize_bar(window, df):
    fig = Figure(figsize=(4.5, 4))
    ax = fig.add_subplot(111)

    # Budget vs Actual bar chart
    budgets = {'Food': 200, 'Entertainment': 100, 'Transportation': 150, 'Bills': 300, 'Education': 100}
    budget_df = pd.DataFrame.from_dict(budgets, orient='index', columns=['Budget'])
    actual = df[(df['Amount'] < 0) & (~df['Category'].isin(['Transfer', 'Refund']))].groupby('Category')[
        'Amount'].sum().abs()
    comparison = budget_df.join(actual.rename('Actual')).fillna(0)

    comparison.plot(kind='bar', ax=ax)


    ax.title.set_text('Budget vs Actual Spending')
    ax.set_xlabel('Category')
    ax.set_ylabel('Amount')
    ax.grid(True, axis='y')

    # Embed the figure into the tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=2, padx=10, pady=10)



# === PIE CHART: Spending by Category ===
def visualize_pie(window,df):

    fig = Figure(figsize=(4, 4))
    ax = fig.add_subplot(111)

    # Filter expenses (negative amounts, exclude Transfers and Refunds)
    expenses = df[(df['Amount'] < 0) & (~df['Category'].isin(['Transfer', 'Refund']))].groupby('Category')[
        'Amount'].sum().abs()
    if expenses.empty:
        ax.text(0.5, 0.5, 'No expenses to display', ha='center', va='center')
        ax.set_title('Spending by Category')
    else:
        expenses.plot(kind='pie',ax=ax, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
        ax.set_ylabel("")
        ax.set_title('Spending by Category')

    # Embed the figure into the tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(column=2, row=2, padx=10, pady=10)

