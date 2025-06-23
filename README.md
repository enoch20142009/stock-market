📊 Financial News Analysis Dashboard
This project explores the relationship between financial news sentiment and stock price movements by consolidating multiple datasets into a single, interactive dashboard. It demonstrates data hygiene, structured workflows, and audit trail logging — key skills aligned with data engineering and insight-driven decision making.

✅ Features
📑 Multi-source Data Integration: Combines financial news (JSON) with stock prices (via yfinance).

🧹 Data Cleaning & Validation: Handles duplicate removal, format normalization, and validation checks.

📝 Full Audit Trail: Logs each transformation step with timestamps, dataset name, row count, and column count (stored in SQLite).

📊 Interactive Visualization Dashboard: Built with Streamlit to explore sentiment impact on stock price movements.

💾 Audit Trail Viewer: Real-time, downloadable audit logs directly within the dashboard.

📂 Project Structure
stock_sentiment_analysis/
├── data/                  # Raw and processed datasets
├── database/              # SQLite database for audit logs
├── notebooks/             # Jupyter or converted scripts for development
├── src/                   # Modular code (audit logging, preprocessing)
├── streamlit_app.py       # Main dashboard application
├── run_all.sh             # Automation script for preprocessing + dashboard
├── requirements.txt
└── README.md

🚀 How to Run Locally
# Clone this repository
git clone https://github.com/yourusername/stock_sentiment_analysis.git
cd stock_sentiment_analysis

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the pipeline and dashboard
bash run_all.sh

