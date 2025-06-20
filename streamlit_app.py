import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# ---------- CONFIG ----------
DB_PATH = 'database/stock_audit.db'
MERGED_DATA_PATH = 'data/merged_dataset.csv'

# ---------- LOAD DATA ----------
@st.cache_data
def load_merged_data():
    return pd.read_csv(MERGED_DATA_PATH)

@st.cache_data
def load_audit_log():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM audit_log ORDER BY timestamp DESC", conn)
    conn.close()
    return df

merged_df = load_merged_data()
audit_log_df = load_audit_log()

# ---------- STREAMLIT UI ----------
st.title("📊 Stock Sentiment Analysis Dashboard")

st.sidebar.header("Filter Options")
selected_ticker = st.sidebar.selectbox("Select Ticker", merged_df['Ticker'].unique())

subset = merged_df[merged_df['Ticker'] == selected_ticker]

st.header(f"Analysis for {selected_ticker}")

# ---------- ANALYSIS A: Hit Rate ----------
pos = subset[subset['sentiment'] == 'positive']
neg = subset[subset['sentiment'] == 'negative']

pos_hit_rate = (pos['daily_diff'] > 0).mean() * 100
neg_hit_rate = (neg['daily_diff'] < 0).mean() * 100

st.subheader("✅ Sentiment Hit Rate Analysis")
st.write(f"Positive Sentiment Hit Rate: **{pos_hit_rate:.2f}%**")
st.write(f"Negative Sentiment Hit Rate: **{neg_hit_rate:.2f}%**")

fig, ax = plt.subplots()
ax.bar(['Positive', 'Negative'], [pos_hit_rate, neg_hit_rate], color=['green', 'red'])
ax.set_ylabel("Accuracy (%)")
ax.set_title("Sentiment Prediction Accuracy")
st.pyplot(fig)

# ---------- ANALYSIS B: Average Return by Sentiment ----------
st.subheader("📊 Average Daily Return by Sentiment")
avg_returns = subset.groupby('sentiment')['daily_diff'].mean()
fig2, ax2 = plt.subplots()
avg_returns.plot(kind='bar', color=['green', 'red'], ax=ax2)
ax2.set_ylabel("Average Daily Return")
ax2.set_title("Average Stock Return by Sentiment")
st.pyplot(fig2)

# ---------- ANALYSIS C: Scatter Plot ----------
st.subheader("📈 Sentiment vs. Daily Price Change")
subset['sentiment_numeric'] = subset['sentiment'].map({'positive': 1, 'negative': -1})
fig3, ax3 = plt.subplots()
ax3.scatter(subset['sentiment_numeric'], subset['daily_diff'], alpha=0.5)
ax3.set_xlabel("Sentiment (+1=Positive, -1=Negative)")
ax3.set_ylabel("Daily Price Change")
ax3.set_title("Sentiment vs. Stock Price Change")
ax3.axhline(0, color='black', linestyle='--')
st.pyplot(fig3)

# ---------- RAW DATA VIEW ----------
with st.expander("🔎 View Raw Merged Dataset"):
    st.dataframe(subset)

# ---------- AUDIT LOG VIEW ----------
st.subheader("📝 Audit Trail")
st.dataframe(audit_log_df)

csv = audit_log_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Audit Log", csv, "audit_log.csv", "text/csv")

# ---------- DATASET SHAPES SUMMARY ----------
if {'dataset_name', 'row_count', 'column_count'}.issubset(audit_log_df.columns):
    st.subheader("📋 Dataset Sizes Logged")
    shape_summary = audit_log_df.sort_values('timestamp').drop_duplicates('dataset_name', keep='last')
    shape_summary = shape_summary[['dataset_name', 'row_count', 'column_count', 'description', 'timestamp']]
    st.dataframe(shape_summary)

st.success("Dashboard Loaded Successfully ✅")
