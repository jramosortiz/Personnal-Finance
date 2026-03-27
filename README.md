
<img width="6912" height="3456" alt="Finance banner" src="https://github.com/user-attachments/assets/0d84f254-d13d-4021-8046-61c3bb31c3ec" />


# Financial Bested
A Python tool that analyzes your bank transactions using Gemini AI and turns them into
graphs, summaries, and actionable financial advice.

---

## Tools
Language                                                     
                                                               
  - Python 3.12                                                
                                                               
  GUI                                                          
                                                               
  - tkinter + ttk — all UI components, dialogs, file pickers   
  - matplotlib + FigureCanvasTkAgg — charts embedded in the GUI
                                                               
  Data                                                         
                                                               
  - pandas — data manipulation and analysis
  - openpyxl — reading .xlsx Excel files
                                                               
  AI / External API                                            
                                                               
  - Google Gemini API (gemini-2.5-flash) via google.genai —    
  transaction categorization + finance Q&A assistant
                                                               
  Config          

  - python-dotenv — loads GEMINI_API_KEY from .env             
   
  Dev Tools                                                    
                  
  - Git — version control
  - PyCharm (JetBrains) — IDE (.idea/ config present)
  - threading — async AI calls so UI doesn't freeze            
   
  Data Storage                                                 
                  
  - No database — data lives in .xlsx files (Chase bank        
  exports) and in-memory pandas DataFrames at runtime
     

---
### Requirements
- Python 3.9+
- Google Gemini API key
- CSV export from your bank

```bash
pip install google-generativeai pandas matplotlib python-dotenv rich
```

---

### Setup
1. Clone the repo and install dependencies
2. Create a .env file with your key:
GEMINI_API_KEY=your_key_here
---

How to Use

---

```bash
python main.py
```
1. **Download gemini api key** - replace api key after "="
2.  **Input your CSV** — export it from your bank and provide the file path
3. **Type your goal** — e.g. “Help me save $5,000 by the end of the year”
4. **Get your report** — graphs, bullet point summaries, and recommendations
5.  **Import from googleApi file** - import google.generativeai as genai, import logging, import os, from dotenv import load_dotenv

