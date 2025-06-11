
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from data_front import get_sentiment_over_time

st.set_page_config(page_title="Corporate Net Sentiment Analysis", layout="wide")
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Corporate Net Sentiment Analysis</h1>", unsafe_allow_html=True)

# --- Ticker/Sector seçimi için örnek liste ---
company_db = {
    "AAPL": {"sector": "Technology"},
    "MSFT": {"sector": "Technology"},
    # Gerekirse buraya yeni şirketler ekleyebilirsin
}
all_tickers = list(company_db.keys())
all_sectors = sorted(set([v["sector"] for v in company_db.values()]))

col1, col2 = st.columns(2)
with col1:
    selected_ticker = st.selectbox("Select Ticker", all_tickers)
with col2:
    selected_sector = st.selectbox("Select Sector", all_sectors)

# --- Data çek ---
df = get_sentiment_over_time(selected_ticker)

if df.empty:
    st.warning("No data available for the selected ticker.")
    st.stop()

# --- Quarter-Year Selectbox ---
quarter_year_options = df["quarter_year"].unique()
selected_quarter = st.selectbox("Select Quarter & Year", quarter_year_options)

# --- Seçili satırı bul ve göster ---
row = df[df["quarter_year"] == selected_quarter]
if row.empty:
    st.warning("No data for the selected quarter.")
    st.stop()
selected_row = row.iloc[0]

colA, colB, colC, colD = st.columns(4)
colA.metric("Quarter-Year", selected_row["quarter_year"])
colB.metric("Net Sentiment", f'{selected_row["net_sentiment"]:.2f}')
colC.metric("Sector", selected_row["sector"])
colD.metric("Ticker", selected_row["ticker"])

st.markdown("---")
st.subheader("All Quarters Table")
st.dataframe(df, use_container_width=True)

# --- Grafik ---
st.subheader("Quarterly Net Sentiment (Bar Chart)")

# Pozitif/negatif renk listesi otomatik oluşturuluyor
colors = ["#00CC96" if val >= 0 else "#EF553B" for val in df["net_sentiment"]]
# Plotly Bar Chart
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df["quarter_year"],
    y=df["net_sentiment"],
    marker_color=colors,
    name='Net Sentiment',
    hovertemplate='Quarter-Year: %{x}<br>Net Sentiment: %{y:.2f}<extra></extra>',
))
fig.update_layout(
    xaxis_title="Quarter-Year",
    yaxis_title="Net Sentiment",
    template="plotly_dark",
    plot_bgcolor="#222A38",
    paper_bgcolor="#222A38",
    font=dict(family="Inter, Arial", size=16),
    bargap=0.25,
    height=450
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==============================================================================
# DEEP-DIVE SENTIMENT ANALYSIS (FinBERT backend ile konuşur)
# ==============================================================================

st.header("Deep-Dive Sentiment Analysis")
st.write("""
Click the button to perform a deep-dive analysis on the backend's default MDA text using FinBERT.
Results will be visualized below.
""")

DEFAULT_MDA_ANALYSIS_URL = "http://127.0.0.1:8000/analyze_default_mda/"  # Gerekirse backend URL'ini değiştir

if st.button("✨ Perform Deep-Dive Analysis"):
    with st.spinner("Connecting to backend and running analysis... Please wait."):
        try:
            response = requests.get(DEFAULT_MDA_ANALYSIS_URL, timeout=300)
            response.raise_for_status()
            data = response.json()
            results = data.get("sentiment_results")

            st.success(f"Analysis Completed! Source: `{data.get('source', 'N/A')}`")
            st.markdown("### Analysis Results")

            labels = ['Positive Paragraphs', 'Negative Paragraphs', 'Neutral Paragraphs']
            values = [
                results.get("count_positive_chunks", 0),
                results.get("count_negative_chunks", 0),
                results.get("count_neutral_chunks", 0)
            ]
            colors = ['#28a745', '#dc3545', '#6c757d']

            fig_pie = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.5,
                marker_colors=colors,
                pull=[0.05, 0, 0]
            )])

            fig_pie.update_layout(
                title_text="Paragraph Sentiment Distribution",
                template="plotly_dark",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            col1, col2 = st.columns([1, 1])

            with col1:
                st.plotly_chart(fig_pie, use_container_width=True)
            with col2:
                st.markdown("#### Key Metrics")
                st.markdown(f"""
                - **Peak Positive Score:** `{results.get("max_positive_score", 0):.4f}`
                - **Peak Negative Score:** `{results.get("max_negative_score", 0):.4f}`
                - **Average Positive Score:** `{results.get("avg_positive", 0):.4f}`
                - **Average Negative Score:** `{results.get("avg_negative", 0):.4f}`
                """)
                total_paragraphs = sum(values)
                st.info(f"A total of **{total_paragraphs}** paragraphs were analyzed.")

            with st.expander("View Raw Dictionary Output"):
                st.json(results)

        except requests.exceptions.RequestException as e:
            st.error(f"API Connection Error: Could not connect to the backend.")
            st.info(f"Details: {e}")

st.markdown("---")

# ==============================================================================
# MD&A SECTION EXTRACTION (SEC API ile metin çekmek)
# ==============================================================================

st.header("MDA Section Extraction from SEC API")
st.write("Click to extract the MD&A section from SEC filings using the SEC API.")

if st.button("✨ Get MDA from SEC API"):
    with st.spinner("Connecting to SEC API and extracting MDA section..."):
        try:
            # Gerçek api_key'i KESİNLİKLE .env dosyasından çekmelisin, burada sabit bırakma!
            from sec_api import ExtractorApi
            extractorApi = ExtractorApi(api_key="YOUR_API_KEY_HERE")  # <---- Buraya kendi key'ini koy
            mda_file_api_test_url_10_q = "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000037996/000003799625000072/f-20250331.htm"
            mda_key_dict = {
                "10-Q": "part1item2",
                "10-K": "7"
            }
            mdna_section = extractorApi.get_section(mda_file_api_test_url_10_q, mda_key_dict['10-Q'], "text")
            st.write(mdna_section)
        except Exception as e:
            st.error(f"API Connection Error: Could not connect to SEC API.")
            st.info(f"Details: {e}")
