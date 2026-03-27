import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import FileReader
import Visualize_Graph

# Color palette
BG         = "#F0F4F8"
CARD_BG    = "#FFFFFF"
ACCENT     = "#4361EE"
ACCENT_DK  = "#3451D1"
TEXT_DARK  = "#1A202C"
TEXT_MUTED = "#718096"
SUCCESS    = "#38A169"
DANGER     = "#E53E3E"
HEADER_BG  = "#1A202C"


def _styled_btn(parent, text, command):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=ACCENT, fg="white", font=("Helvetica", 11, "bold"),
        relief="flat", cursor="hand2", padx=24, pady=10, bd=0,
        activebackground=ACCENT_DK, activeforeground="white"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_DK))
    btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))
    return btn


def upload_file(window, file_label, status_dot):
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
    )

    if not file_path:
        return

    short_name = file_path.split("/")[-1]
    file_label.configure(text=f"Loading: {short_name}...", fg=TEXT_MUTED)
    window.update()

    try:
        df = FileReader.load_TransactionFile(file_path)
        for widget in window.winfo_children():
            widget.destroy()
        mainWindow(window, df)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file:\n{e}")
        file_label.configure(text="No file selected", fg=TEXT_MUTED)
        print(f"Error: {e}")


def upload_Window():
    window = tk.Tk()
    window.title("Personal Finance")
    window.geometry("560x380")
    window.configure(bg=BG)
    window.resizable(False, False)
    window.eval("tk::PlaceWindow . center")

    # Header
    header = tk.Frame(window, bg=HEADER_BG, height=65)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="Personal Finance", font=("Helvetica", 18, "bold"),
             bg=HEADER_BG, fg="white").pack(expand=True)

    # Card
    card = tk.Frame(window, bg=CARD_BG, padx=50, pady=35)
    card.pack(expand=True)

    tk.Label(card, text="Import Your Transactions",
             font=("Helvetica", 14, "bold"), bg=CARD_BG, fg=TEXT_DARK).pack()

    tk.Label(card, text="Supports .xlsx and .csv bank exports",
             font=("Helvetica", 10), bg=CARD_BG, fg=TEXT_MUTED).pack(pady=(4, 22))

    # Drop-zone look
    drop_frame = tk.Frame(card, bg="#EBF4FF", bd=2, relief="groove",
                          padx=30, pady=18)
    drop_frame.pack(fill="x", pady=(0, 18))

    status_dot = tk.Label(drop_frame, text="●", font=("Helvetica", 10),
                          bg="#EBF4FF", fg=TEXT_MUTED)
    status_dot.pack()

    file_label = tk.Label(drop_frame, text="No file selected",
                          font=("Helvetica", 10), bg="#EBF4FF", fg=TEXT_MUTED,
                          wraplength=320)
    file_label.pack()

    _styled_btn(card, "  Choose File  ",
                command=lambda: upload_file(window, file_label, status_dot)).pack()

    window.mainloop()


def _stat_card(parent, label, value, color):
    card = tk.Frame(parent, bg=CARD_BG, padx=18, pady=14)
    card.pack(side="left", padx=8, expand=True, fill="both")
    tk.Label(card, text=label, font=("Helvetica", 9),
             bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w")
    tk.Label(card, text=f"${value:,.2f}", font=("Helvetica", 20, "bold"),
             bg=CARD_BG, fg=color).pack(anchor="w")


def mainWindow(window, df):
    window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
    window.configure(bg=BG)
    window.resizable(True, True)

    # ── Header ──────────────────────────────────────────────────────────
    header = tk.Frame(window, bg=HEADER_BG, height=55)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="Personal Finance  Dashboard",
             font=("Helvetica", 15, "bold"),
             bg=HEADER_BG, fg="white").pack(side="left", padx=24)

    # ── Summary cards ───────────────────────────────────────────────────
    total_income = df[df['Amount'] > 0]['Amount'].sum()
    total_spent  = df[df['Amount'] < 0]['Amount'].sum()
    net          = total_income + total_spent

    summary = tk.Frame(window, bg=BG, pady=12)
    summary.pack(fill="x", padx=20)
    _stat_card(summary, "Total Income",  total_income,     SUCCESS)
    _stat_card(summary, "Total Spent",   abs(total_spent), DANGER)
    _stat_card(summary, "Net Balance",   net, ACCENT if net >= 0 else DANGER)

    # ── Content area ────────────────────────────────────────────────────
    content = tk.Frame(window, bg=BG)
    content.pack(fill="both", expand=True, padx=20, pady=(0, 12))

    # Left – transaction table
    left = tk.Frame(content, bg=CARD_BG, padx=12, pady=12)
    left.pack(side="left", fill="both", padx=(0, 10))

    tk.Label(left, text="Transactions", font=("Helvetica", 11, "bold"),
             bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("T.Treeview",
                    background=CARD_BG, foreground=TEXT_DARK,
                    rowheight=26, fieldbackground=CARD_BG,
                    font=("Helvetica", 10))
    style.configure("T.Treeview.Heading",
                    font=("Helvetica", 10, "bold"),
                    background=BG, foreground=TEXT_DARK, relief="flat")
    style.map("T.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    tree_wrap = tk.Frame(left, bg=CARD_BG)
    tree_wrap.pack(fill="both", expand=True)

    vsb = ttk.Scrollbar(tree_wrap, orient="vertical")
    vsb.pack(side="right", fill="y")

    table = ttk.Treeview(
        tree_wrap, show="headings", style="T.Treeview",
        columns=["Description", "Category", "Amount"],
        yscrollcommand=vsb.set, height=20
    )
    table.pack(side="left", fill="both")
    vsb.config(command=table.yview)

    table.heading("Description", text="Description")
    table.heading("Category",    text="Category")
    table.heading("Amount",      text="Amount")
    table.column("Description",  width=230)
    table.column("Category",     width=130, anchor="center")
    table.column("Amount",       width=90,  anchor="e")

    for row in range(df.index.size):
        vals   = df.loc[row, ["Description", "Category", "Amount"]].tolist()
        amount = vals[2]
        tag    = "expense" if amount < 0 else "income"
        table.insert("", "end", values=vals, tags=(tag,))

    table.tag_configure("expense", foreground=DANGER)
    table.tag_configure("income",  foreground=SUCCESS)

    # Right – charts
    right = tk.Frame(content, bg=BG)
    right.pack(side="left", fill="both", expand=True)

    right.grid_columnconfigure(0, weight=1)
    right.grid_columnconfigure(1, weight=1)

    Visualize_Graph.visualize_pie(right, df)
    Visualize_Graph.visualize_bar(right, df)
    Visualize_Graph.visualize_line(right, df)
