import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from data_front import get_sentiment_over_time, TEST_MDA_TEXT
from sec_api import ExtractorApi

#glibal
call_sec_api = False
mdna_section = ""

BACKEND_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Corporate Net Sentiment Analysis", layout="wide")
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Corporate Net Sentiment Analysis</h1>", unsafe_allow_html=True)

# --- 1. SEC Links & Company Database ---
company_db = {
    "mcd": {
        "name": "McDonald's",
        "sector": "Consumer Cyclical",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000063908/000006390825000025/mcd-20250331.htm"
    },
    "mtch": {
        "name": "Match Group",
        "sector": "Communication Services",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000891103/000089110325000076/mtch-20250331.htm"
    },
    "lyv": {
        "name": "Live Nation",
        "sector": "Communication Services",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0001335258/000133525825000055/lyv-20250331.htm"
    },
    "bby": {
        "name": "Best Buy",
        "sector": "Consumer Cyclical",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000764478/000076447825000019/bby-20250503x10q.htm"
    },
    "ba": {
        "name": "Boeing",
        "sector": "Industrials",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000012927/000001292725000031/ba-20250331.htm"
    },
    "tsla": {
        "name": "Tesla",
        "sector": "Consumer Discretionary",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0001318605/000162828025018911/tsla-20250331.htm"
    },
    "xom": {
        "name": "Exxon Mobil",
        "sector": "Energy",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000034088/000003408825000024/xom-20250331.htm"
    },
    "cmg": {
        "name": "Chipotle",
        "sector": "Consumer Cyclical",
        "sec_url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0001058090/000105809025000031/cmg-20250331.htm"
    }
}

all_tickers = list(company_db.keys())
ticker_names = [f"{company_db[t]['name']} ({t.upper()})" for t in all_tickers]
ticker_label_to_ticker = {f"{company_db[t]['name']} ({t.upper()})": t for t in all_tickers}

# --- 2. Company Selectbox ---
selected_label = st.selectbox("Select Company", ticker_names)
selected_ticker = ticker_label_to_ticker[selected_label]
selected_sector = company_db[selected_ticker]["sector"]
selected_sec_url = company_db[selected_ticker]["sec_url"]

# --- 3. Net Sentiment Data (Dummy, can be replaced with real) ---
df = get_sentiment_over_time(selected_ticker.upper())

if df.empty:
    st.warning("No data available for the selected ticker.")
    st.stop()

# --- 4. Quarter-Year Selectbox ---
quarter_year_options = df["quarter_year"].unique()
selected_quarter = st.selectbox("Select Quarter & Year", quarter_year_options)

row = df[df["quarter_year"] == selected_quarter]
if row.empty:
    st.warning("No data for the selected quarter.")
    st.stop()
selected_row = row.iloc[0]

colA, colB, colC, colD = st.columns(4)
colA.metric("Quarter-Year", selected_row["quarter_year"])
colB.metric("Net Sentiment", f'{selected_row["net_sentiment"]:.2f}')
colC.metric("Sector", selected_row["sector"])
colD.metric("Ticker", selected_ticker.upper())

st.markdown("---")
st.subheader("All Quarters Table")
st.dataframe(df, use_container_width=True)

# --- 5. Modern Bar Chart (Up Green / Down Red) ---
st.subheader("Quarterly Net Sentiment (Bar Chart)")
colors = ["#00CC96" if val >= 0 else "#EF553B" for val in df["net_sentiment"]]

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


# --- 7. MDA Section Extraction from SEC API ---
st.header("MDA Section Extraction from SEC API")
st.write(
    f"Click to extract the MD&A section from SEC filings using the SEC API. "
    f"(Selected company: **{company_db[selected_ticker]['name']}**, SEC Filing: [link]({selected_sec_url}))"
)

if st.button("✨ Get MDA from SEC API"):
    with st.spinner("Connecting to SEC API and extracting MDA section..."):
        try:
            if call_sec_api:
                extractorApi = ExtractorApi(api_key="ac9ba652b06eae03d5f550d0585e3f9fdabaa36f186482b6f31f0d449514ff6b")  # Buraya kendi keyini koy
                mda_file_api_test_url_10_q = selected_sec_url
                mda_key_dict = {
                    "10-Q": "part1item2",
                    "10-K": "7"
                }
                # Not: Örnek olarak tüm linkler 10-Q gibi varsayılmıştır!
                mdna_section = extractorApi.get_section(mda_file_api_test_url_10_q, mda_key_dict['10-Q'], "text")
            else:
                print("working with hardcoded TEST_MDA_TEXT")
                mdna_section = TEST_MDA_TEXT
            st.write(mdna_section)
        except Exception as e:
            st.error(f"API Connection Error: Could not connect to SEC API.")
            st.info(f"Details: {e}")



# --- 6. Deep-Dive Sentiment Analysis (FinBERT/Backend) ---
st.header("Deep-Dive Sentiment Analysis")
st.write("""
Click the button to perform a deep-dive analysis on the backend's default MDA text using FinBERT.
Results will be visualized below.
""")

DEFAULT_MDA_ANALYSIS_URL = "http://127.0.0.1:8000/analyze_default_mda/"  # Gerekirse backend URL'ini değiştir
mda_analyse_url = 'http://127.0.0.1:8000/analyze_mda'

if st.button("✨ Perform Deep-Dive Analysis"):
    with st.spinner("Connecting to backend and running analysis... Please wait."):
        try:
            #params shoud be body...
            params = {"mda_text": mdna_section}  # Burada TEST_MDA_TEXT'i kullanıyoruz
            response = requests.post(mda_analyse_url, params=params, timeout=300)
            response.raise_for_status()
            data = response.json()
            results = data.get("sentiment_results")

            print("sentiment:", results)
            st.write(results)
            st.success(f"Analysis Completed! Source: `{data.get('source', 'N/A')}`")
            st.markdown("### Analysis Results")

            labels = ['Positive Paragraphs', 'Negative Paragraphs', 'Neutral Paragraphs']
            values = [
                results.get("count_positive_chunks", 0),
                results.get("count_negative_chunks", 0),
                results.get("count_neutral_chunks", 0)
            ]
            pie_colors = ['#28a745', '#dc3545', '#6c757d']

            fig_pie = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.5,
                marker_colors=pie_colors,
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
#prediction
st.header("Deep-Dive Prediction")
st.write("""
Click the button to perform a deep-dive analysis on the backend's default MDA text using FinBERT.
Results will be visualized below.
""")

prediction_endpoint = f"{BACKEND_BASE_URL}/get_prediction_from_sentiment_processed"

if st.button("✨ Get prediction"):
    with st.spinner("Connecting to backend and running prediction... Please wait."):
        try:
            X_new = pd.DataFrame([{
                'net_sentiment': -0.1,
                'industry': 'Auto Manufacturers',
                'q_num': "4",
                'neutral_dominance': False
                }])
            X_new = X_new.astype({
                'q_num': 'object',
                'neutral_dominance': 'object'
            })

            #params shoud be body...
            params = {"X_new": X_new.iloc[0].to_dict()}  # Burada TEST_MDA_TEXT'i kullanıyoruz
            print("params", params)
            print(X_new.columns)
            response = requests.get(prediction_endpoint, params=X_new.iloc[0].to_dict(), timeout=300)
            response.raise_for_status()
            data = response.json()
            prediction = data.get("prediction")

            print("prediction:", prediction)
            st.write(prediction)
            st.success(f"Analysis Completed! Source: `{data.get('source', 'N/A')}`")
            st.markdown("### Analysis Results")
        except Exception as e:
            print("something went wrong", e)
