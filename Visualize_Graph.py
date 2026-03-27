from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
import pandas as pd

# Chart styling
COLORS   = ["#4361EE", "#38A169", "#E53E3E", "#F6AD55", "#9F7AEA",
            "#38BDF8", "#FB923C", "#A3E635"]
BG_CHART = "#FFFFFF"
GRID_CLR = "#E2E8F0"
TEXT_CLR = "#1A202C"
TITLE_SZ = 10

mpl.rcParams.update({
    "font.family":       "Helvetica",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.facecolor":    BG_CHART,
    "figure.facecolor":  BG_CHART,
    "text.color":        TEXT_CLR,
    "axes.labelcolor":   TEXT_CLR,
    "xtick.color":       TEXT_CLR,
    "ytick.color":       TEXT_CLR,
    "axes.grid":         True,
    "grid.color":        GRID_CLR,
    "grid.linewidth":    0.8,
})


def _embed(fig, parent, col, row, colspan=1):
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().grid(
        column=col, row=row, columnspan=colspan,
        padx=6, pady=6, sticky="nsew"
    )


def visualize_pie(window, df):
    expenses = (
        df[(df['Amount'] < 0) & (~df['Category'].isin(['Transfer', 'Refund']))]
        .groupby('Category')['Amount'].sum().abs()
    )

    fig = Figure(figsize=(4.2, 3.8))
    ax  = fig.add_subplot(111)

    if expenses.empty:
        ax.text(0.5, 0.5, 'No expenses to display', ha='center', va='center')
    else:
        wedges, texts, autotexts = ax.pie(
            expenses, labels=expenses.index, autopct='%1.1f%%',
            colors=COLORS[:len(expenses)], startangle=140,
            wedgeprops={"linewidth": 1.5, "edgecolor": "white"}
        )
        for t in autotexts:
            t.set_fontsize(8)
        ax.set_ylabel("")

    ax.set_title("Spending by Category", fontsize=TITLE_SZ, fontweight="bold", pad=10)
    fig.tight_layout()
    _embed(fig, window, col=0, row=0)


def visualize_bar(window, df):
    budgets = {
        'Food': 200, 'Entertainment': 100,
        'Transportation': 150, 'Bills': 300, 'Education': 100
    }
    budget_df = pd.DataFrame.from_dict(budgets, orient='index', columns=['Budget'])
    actual    = (
        df[(df['Amount'] < 0) & (~df['Category'].isin(['Transfer', 'Refund']))]
        .groupby('Category')['Amount'].sum().abs()
    )
    comparison = budget_df.join(actual.rename('Actual')).fillna(0)

    fig = Figure(figsize=(4.2, 3.8))
    ax  = fig.add_subplot(111)

    x     = range(len(comparison))
    width = 0.38
    ax.bar([i - width/2 for i in x], comparison['Budget'],
           width=width, label='Budget', color="#4361EE", alpha=0.85)
    ax.bar([i + width/2 for i in x], comparison['Actual'],
           width=width, label='Actual',  color="#E53E3E", alpha=0.85)

    ax.set_xticks(list(x))
    ax.set_xticklabels(comparison.index, rotation=25, ha="right", fontsize=8)
    ax.set_ylabel("Amount ($)", fontsize=9)
    ax.set_title("Budget vs Actual Spending", fontsize=TITLE_SZ, fontweight="bold", pad=10)
    ax.legend(fontsize=8, framealpha=0)
    ax.grid(axis="x", alpha=0)
    fig.tight_layout()
    _embed(fig, window, col=1, row=0)


def visualize_line(window, df):
    df = df.copy()
    df['Posting Date'] = pd.to_datetime(df['Posting Date'], format='%m/%Y', errors='coerce')
    df_sorted = df.dropna(subset=['Posting Date']).sort_values('Posting Date')

    fig = Figure(figsize=(8.8, 3.4))
    ax  = fig.add_subplot(111)

    ax.plot(df_sorted['Posting Date'], df_sorted['Balance'],
            marker='o', markersize=4, color="#4361EE",
            linewidth=2, label='Balance')
    ax.fill_between(df_sorted['Posting Date'], df_sorted['Balance'],
                    alpha=0.08, color="#4361EE")

    ax.set_xlabel("Date", fontsize=9)
    ax.set_ylabel("Balance ($)", fontsize=9)
    ax.set_title("Balance Over Time", fontsize=TITLE_SZ, fontweight="bold", pad=10)
    fig.autofmt_xdate(rotation=25)
    fig.tight_layout()
    _embed(fig, window, col=0, row=1, colspan=2)
