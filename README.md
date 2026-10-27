# FinWise AI — runnable FinTech startup prototype

## Requirements
- Python 3.10 or newer
- Internet connection for initial package installation

## Run locally
1. Extract the ZIP.
2. Open a terminal in the `FinWise_AI_Startup` folder.
3. Create a virtual environment (recommended):
   - Windows: `py -m venv .venv`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Start app: `streamlit run app.py`
6. Open the local URL shown in the terminal (usually http://localhost:8501).

## What is included
- Interactive personal budget/savings demo
- Editable five-year revenue and expense forecast
- Profit/loss and first profitable year calculation
- Capital funding mix calculator
- Future API architecture and privacy notes

All default financial numbers are illustrative assumptions. The app does not connect to banks, transfer money, approve loans, or provide regulated financial advice.
