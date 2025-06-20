echo "⚙️ Creating SQL Database for auditing..."
python src/audit_logging.py

echo "⚙️ Running preprocessing pipeline..."
python notebooks/financial_news_stock_price.py

echo "🚀 Launching Streamlit dashboard..."
python -m streamlit run streamlit_app.py


