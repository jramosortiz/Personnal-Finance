import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import FileReader
import Visualize_Graph


def upload_file(window, file_label):
    progressBar = ttk.Progressbar(window, mode='determinate',length=300)
    progressBar.grid(column=1, row=2)


    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    progressBar.start()  # start progress bar

    if file_path:

        try:


            file_label.configure(text=file_path) # show file path into windows


            #Sent to be parse into pandas
            df = FileReader.load_TransactionFile(file_path)


            progressBar.stop() #Stop the progress bar

            # Destroy all widgets except the window itself
            for widget in window.winfo_children():
                widget.destroy()

            #Once everything was parse into pandas. Open main menu window.
            mainWindow(window, df)


        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")#show any errors
            print(f"Error: {e}")

    else:
        print("Uploading File failed")




def upload_Window():
    #basic window configuration
    window = tk.Tk()
    window.title("Personal Finance")
    window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")

    # make the grid stretch
    for i in range(4):
        window.grid_rowconfigure(i, weight=1)
    for i in range(3):
        window.grid_columnconfigure(i, weight=1)

    window.resizable(True, True)
    window.configure(background="#B2D3C2")

    file_label = ttk.Label(window, text="No file selected", wraplength=250,background="#B2D3C2")
    file_label.grid(column=1, row=0)



    #get select files to be read by panda
    upload_button = ttk.Button(window, text="Get File", command=lambda: upload_file(window, file_label))
    upload_button.grid(column=1, row=1)


    window.mainloop()







def mainWindow(window, df):

    #Welcome Label
    welcome_label = tk.Label(window, text="Welcome to Personal Finance", font=("Arial", 20), bg="#B2D3C2")
    welcome_label.grid(column=1,row=0)



    #Generate table with money spent
    finance_Table = ttk.Treeview(window, show="headings", columns=["Description", "Category","Amount"])
    finance_Table.grid(column=0 ,row=1)

    #Get df columns and index values
    df_col = df.columns.values
    df_row = df.index.size

    #Create the header with values
    finance_Table.heading("Description", text="Description")
    finance_Table.heading("Category", text="Category")
    finance_Table.heading("Amount", text="Amount")

    #Center the selected columns
    finance_Table.column("Amount", anchor="e")
    finance_Table.column("Category", anchor="center")

    #for loop that create the row with information about the purchase
    for row in range(df_row):
        finance_Table.insert("","end",values=df.loc[row,["Description","Category","Amount"]].tolist())

    #Create Pie table
    Visualize_Graph.visualize_pie(window,df)

    #Create Bar table
    Visualize_Graph.visualize_bar(window,df)

    # Create Bar table
    Visualize_Graph.visualize_line(window,df)





upload_Window()