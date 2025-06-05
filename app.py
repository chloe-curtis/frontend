import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Quarterly Sentiment Analysis", layout="wide")
st.markdown(
    "<h1 style='margin-bottom: 1.5rem;'>Corporate Quarterly Sentiment Analysis</h1>",
    unsafe_allow_html=True
)

# Örnek şirket ve sektör verisi
company_db = {
    "AAPL": {"sector": "Technology", "years": [2021, 2022, 2023]},
    "TSLA": {"sector": "Automotive", "years": [2022, 2023, 2024]},
    "MSFT": {"sector": "Technology", "years": [2021, 2022, 2023]},
    "GOOGL": {"sector": "Technology", "years": [2023, 2024]},
    "AMZN": {"sector": "Retail", "years": [2023, 2024]}
}
sectors = sorted(set([v["sector"] for v in company_db.values()]))
quarters = ["Q1", "Q2", "Q3", "Q4"]

# --- Filtreler (aktif, otomatik) ---
col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="large")
with col2:
    selected_sector = st.selectbox("By Sector", sectors)
with col1:
    # Sektöre göre ticker listesi filtreleniyor
    tickers = [k for k, v in company_db.items() if v["sector"] == selected_sector]
    ticker = st.selectbox("By Ticker", tickers)
with col3:
    year = st.selectbox("By Year", company_db[ticker]["years"])
with col4:
    timeframe = st.selectbox("Timeframe (Quarter)", quarters)

st.markdown("---")

# --- Dummy Quarterly Sentiment & News Data ---
np.random.seed(hash(f"{ticker}{year}") % 2**32)
quarter_data = []
for q in quarters:
    pos = np.random.randint(30, 70)
    neu = np.random.randint(10, 40)
    neg = max(0, 100 - pos - neu)
    total_news = np.random.randint(50, 150)
    quarter_data.append({
        "Quarter": q,
        "%Positive": pos,
        "%Neutral": neu,
        "%Negative": neg,
        "Total News": total_news
    })
df = pd.DataFrame(quarter_data)

# --- Renkli Metrikler ---
selected_row = df[df["Quarter"] == timeframe].iloc[0]
colA, colB, colC, colD = st.columns(4)
colA.metric("Quarter", timeframe)
colB.metric("Positive (%)", selected_row["%Positive"])
colC.metric("Neutral (%)", selected_row["%Neutral"])
colD.metric("Negative (%)", selected_row["%Negative"])

# --- Plotly ile Sentiment Trend Grafik ---
st.subheader(f"{ticker} - {year} Quarterly Sentiment Trends")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Quarter"], y=df["%Positive"],
    mode='lines+markers',
    name='%Positive',
    line=dict(color='green', width=3),
    marker=dict(size=10)
))
fig.add_trace(go.Scatter(
    x=df["Quarter"], y=df["%Neutral"],
    mode='lines+markers',
    name='%Neutral',
    line=dict(color='gray', width=3, dash='dash'),
    marker=dict(size=10)
))
fig.add_trace(go.Scatter(
    x=df["Quarter"], y=df["%Negative"],
    mode='lines+markers',
    name='%Negative',
    line=dict(color='red', width=3, dash='dot'),
    marker=dict(size=10)
))

# En yüksek %Positive noktası işaretli
max_idx = df["%Positive"].idxmax()
fig.add_annotation(
    x=df.loc[max_idx, "Quarter"], y=df.loc[max_idx, "%Positive"],
    text="Peak Positive",
    showarrow=True, arrowhead=1, ax=0, ay=-40, bgcolor="white"
)

fig.update_layout(
    xaxis_title="Quarter",
    yaxis_title="Sentiment %",
    legend_title="Sentiment Type",
    plot_bgcolor='#18191A',
    paper_bgcolor='#18191A',
    font=dict(color="white"),
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# --- Detaylı Tablo + Most Frequent Sentiment ---
st.subheader(f"Quarterly Sentiment Table ({ticker} - {year})")
df_table = df.copy()
df_table["Most Frequent Sentiment"] = df_table[["%Positive", "%Neutral", "%Negative"]].idxmax(axis=1).str.replace('%', '')
st.dataframe(df_table, use_container_width=True)

# --- Toplam Haber ---
total_news_year = int(df["Total News"].sum())
st.success(f"**Total News in {year}: {total_news_year}**")

st.caption("All values are randomly generated for demo. Real data/API can be easily integrated.")
