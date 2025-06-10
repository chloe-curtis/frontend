# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import plotly.graph_objects as go
# # import requests

# # #backend api url
# # url = "https://corporate-sentiment-tracker-217305741515.europe-west1.run.app/"
# # # #test backend root
# # # response=requests.get(url)
# # # response_json = response.json()
# # # st.markdown(f"public api root output: {response_json['message']}")

# # st.set_page_config(page_title="Quarterly Sentiment Analysis", layout="wide")
# # st.markdown(
# #     "<h1 style='margin-bottom: 1.5rem;'>Corporate Quarterly Sentiment Analysis</h1>",
# #     unsafe_allow_html=True
# # )

# # # Örnek şirket ve sektör verisi
# # company_db = {
# #     "AAPL": {"sector": "Technology", "years": [2021, 2022, 2023]},
# #     "TSLA": {"sector": "Automotive", "years": [2022, 2023, 2024]},
# #     "MSFT": {"sector": "Technology", "years": [2021, 2022, 2023]},
# #     "GOOGL": {"sector": "Technology", "years": [2023, 2024]},
# #     "AMZN": {"sector": "Retail", "years": [2023, 2024]}
# # }
# # sectors = sorted(set([v["sector"] for v in company_db.values()]))
# # quarters = ["Q1", "Q2", "Q3", "Q4"]

# # # --- Filtreler (aktif, otomatik) ---
# # col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="large")
# # with col2:
# #     selected_sector = st.selectbox("By Sector", sectors)
# # with col1:
# #     # Sektöre göre ticker listesi filtreleniyor
# #     tickers = [k for k, v in company_db.items() if v["sector"] == selected_sector]
# #     ticker = st.selectbox("By Ticker", tickers)
# # with col3:
# #     year = st.selectbox("By Year", company_db[ticker]["years"])
# # with col4:
# #     timeframe = st.selectbox("Timeframe (Quarter)", quarters)

# # st.markdown("---")

# # # --- Dummy Quarterly Sentiment & News Data ---
# # np.random.seed(hash(f"{ticker}{year}") % 2**32)
# # quarter_data = []
# # for q in quarters:
# #     pos = np.random.randint(30, 70)
# #     neu = np.random.randint(10, 40)
# #     neg = max(0, 100 - pos - neu)
# #     total_news = np.random.randint(50, 150)
# #     quarter_data.append({
# #         "Quarter": q,
# #         "%Positive": pos,
# #         "%Neutral": neu,
# #         "%Negative": neg,
# #         "Total News": total_news
# #     })
# # df = pd.DataFrame(quarter_data)

# # # --- Renkli Metrikler ---
# # selected_row = df[df["Quarter"] == timeframe].iloc[0]
# # colA, colB, colC, colD = st.columns(4)
# # colA.metric("Quarter", timeframe)
# # colB.metric("Positive (%)", selected_row["%Positive"])
# # colC.metric("Neutral (%)", selected_row["%Neutral"])
# # colD.metric("Negative (%)", selected_row["%Negative"])

# # # --- Plotly ile Sentiment Trend Grafik ---
# # st.subheader(f"{ticker} - {year} Quarterly Sentiment Trends")

# # fig = go.Figure()
# # fig.add_trace(go.Scatter(
# #     x=df["Quarter"], y=df["%Positive"],
# #     mode='lines+markers',
# #     name='%Positive',
# #     line=dict(color='green', width=3),
# #     marker=dict(size=10)
# # ))
# # fig.add_trace(go.Scatter(
# #     x=df["Quarter"], y=df["%Neutral"],
# #     mode='lines+markers',
# #     name='%Neutral',
# #     line=dict(color='gray', width=3, dash='dash'),
# #     marker=dict(size=10)
# # ))
# # fig.add_trace(go.Scatter(
# #     x=df["Quarter"], y=df["%Negative"],
# #     mode='lines+markers',
# #     name='%Negative',
# #     line=dict(color='red', width=3, dash='dot'),
# #     marker=dict(size=10)
# # ))

# # # En yüksek %Positive noktası işaretli
# # max_idx = df["%Positive"].idxmax()
# # fig.add_annotation(
# #     x=df.loc[max_idx, "Quarter"], y=df.loc[max_idx, "%Positive"],
# #     text="Peak Positive",
# #     showarrow=True, arrowhead=1, ax=0, ay=-40, bgcolor="white"
# # )

# # fig.update_layout(
# #     xaxis_title="Quarter",
# #     yaxis_title="Sentiment %",
# #     legend_title="Sentiment Type",
# #     plot_bgcolor='#18191A',
# #     paper_bgcolor='#18191A',
# #     font=dict(color="white"),
# #     height=400
# # )
# # st.plotly_chart(fig, use_container_width=True)

# # # --- Detaylı Tablo + Most Frequent Sentiment ---
# # st.subheader(f"Quarterly Sentiment Table ({ticker} - {year})")
# # df_table = df.copy()
# # df_table["Most Frequent Sentiment"] = df_table[["%Positive", "%Neutral", "%Negative"]].idxmax(axis=1).str.replace('%', '')
# # st.dataframe(df_table, use_container_width=True)

# # # --- Toplam Haber ---
# # total_news_year = int(df["Total News"].sum())
# # st.success(f"**Total News in {year}: {total_news_year}**")

# # st.caption("All values are randomly generated for demo. Real data/API can be easily integrated.")



# # # --- Full MDA Sentiment Analysis Section (ENGLISH UI) ---
# # st.markdown("---")
# # st.header("Run Sentiment Analysis on Full MDA Text")

# # st.write("""
# # Click the button below to run FinBERT-based sentiment analysis on the full quarterly Management Discussion & Analysis (MDA) text.
# # You will see detailed sentiment statistics for the selected company and year.
# # """)





# # if st.button("Run Sentiment Analysis"):
# #     with st.spinner("Analyzing the MDA text..."):
# #         url = "http://localhost:8000/get_sentiment"  # Update to your backend endpoint
# #         response = requests.get(url)
# #         if response.status_code == 200:
# #             result = response.json()
# #             # Show the analyzed text as well
# #             st.subheader("Analyzed MDA Text")
# #             # Burada analiz edilen metni gösteriyoruz
# #             # Eğer backend'den dönüyorsa: result["text"] veya doğrudan TEST_MDA
# #             st.code(result.get("text", "MDA text not found in API response!"), language="markdown")

# #             st.subheader("FinBERT Sentiment Analysis Results")
# #             st.json(result)
# #         else:
# #             st.error(f"API error! Status code: {response.status_code}")





# # #backend connection test
# # st.markdown("---")

# # #make api call to backend

# # #REMOVE BEFORE DEPLOYMENT
# # url = "http://localhost:8000/"  # For local testing, change to your backend URL
# # response=requests.get(url)
# # response_json = response.json()
# # st.markdown(f"local api test output: {response_json['message']}")

# # # --- Quarter bazında Yorumlar ve Sentiment Score Tablosu ---

# # # Dummy haber/headline + sentiment örnek verisi (her quarter için)
# # quarter_news = {
# #     "Q1": [
# #         {"headline": "Apple launches new product, stocks surge", "sentiment_score": 0.75, "label": "positive", "confidence": 0.91},
# #         {"headline": "R&D investments pay off for AAPL", "sentiment_score": 0.65, "label": "positive", "confidence": 0.82}
# #     ],
# #     "Q2": [
# #         {"headline": "iPhone supply chain faces disruptions", "sentiment_score": -0.4, "label": "negative", "confidence": 0.77},
# #         {"headline": "Apple faces lawsuit over patent", "sentiment_score": -0.5, "label": "negative", "confidence": 0.83}
# #     ],
# #     "Q3": [
# #         {"headline": "Apple announces major update at WWDC", "sentiment_score": 0.52, "label": "positive", "confidence": 0.68},
# #         {"headline": "Mixed reactions to new Macbook", "sentiment_score": 0.12, "label": "neutral", "confidence": 0.58}
# #     ],
# #     "Q4": [
# #         {"headline": "Holiday sales boost revenue", "sentiment_score": 0.88, "label": "positive", "confidence": 0.93},
# #         {"headline": "Concerns over slowing global demand", "sentiment_score": -0.2, "label": "neutral", "confidence": 0.61}
# #     ]
# # }

# # st.subheader(f"{timeframe} - Detailed News Sentiment Table")
# # # Seçilen quarter'ın haberlerini tabloya çevir
# # selected_news = pd.DataFrame(quarter_news[timeframe])
# # st.dataframe(selected_news, use_container_width=True)


# # #get text

# # #use api to get sentiment from text
# # url = "http://localhost:8000/get_sentiment"  # For local testing, change to your backend URL
# # response= requests.get(url)
# # response_json = response.json()
# # st.markdown(f"local api test sentiment output: {response_json}")





# ##########################################################

# # app.py (Tam ve Eksiksiz Versiyon)

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import requests

# # --- Sayfa Yapılandırması ve Başlık ---
# st.set_page_config(page_title="Corporate Sentiment Analysis", layout="wide")
# st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Corporate Sentiment Analysis</h1>", unsafe_allow_html=True)

# # --- Backend URL'leri ---
# DEFAULT_MDA_ANALYSIS_URL = "http://127.0.0.1:8000/analyze_default_mda/"

# #==============================================================================
# # BÖLÜM 1: ÇEYREK BAZLI TREND GÖSTERGE PANELİ (EKSİKSİZ HALİ)
# #==============================================================================
# st.header("Quarterly Sentiment Trends (Dummy Data)")

# # --- Veri Ayarları ---
# company_db = {
#     "AAPL": {"sector": "Technology", "years": [2021, 2022, 2023]},
#     "TSLA": {"sector": "Automotive", "years": [2022, 2023, 2024]},
#     "MSFT": {"sector": "Technology", "years": [2021, 2022, 2023]},
# }
# sectors = sorted(list(set(v["sector"] for v in company_db.values())))
# quarters = ["Q1", "Q2", "Q3", "Q4"]

# @st.cache_data
# def get_sentiment_data(ticker, year):
#     """Bu fonksiyon test amaçlı sahte veri üretir."""
#     np.random.seed(hash(f"{ticker}{year}") % (2**32 - 1))
#     quarter_data = []
#     for q in quarters:
#         pos, neu = np.random.randint(40, 75), np.random.randint(10, 25)
#         neg = 100 - pos - neu
#         quarter_data.append({"Quarter": q, "%Positive": pos, "%Neutral": neu, "%Negative": neg})
#     return pd.DataFrame(quarter_data)

# # --- Filtreler ---
# col1, col2, col3, col4 = st.columns(4)
# with col2:
#     selected_sector = st.selectbox("By Sector", sectors)
# with col1:
#     tickers_in_sector = [k for k, v in company_db.items() if v["sector"] == selected_sector]
#     ticker = st.selectbox("By Ticker", tickers_in_sector)
# with col3:
#     year = st.selectbox("By Year", company_db[ticker]["years"])
# with col4:
#     timeframe = st.selectbox("Timeframe (Quarter)", quarters)

# st.markdown("---")

# # --- Gösterge Paneli Ana Mantığı ---
# df = get_sentiment_data(ticker, year)
# if not df.empty:
#     selected_row = df[df["Quarter"] == timeframe].iloc[0]
#     colA, colB, colC, colD = st.columns(4)
#     colA.metric("Quarter", timeframe)
#     colB.metric("Positive (%)", f'{selected_row["%Positive"]:.0f}')
#     colC.metric("Neutral (%)", f'{selected_row["%Neutral"]:.0f}')
#     colD.metric("Negative (%)", f'{selected_row["%Negative"]:.0f}')

#     st.markdown("<hr style='margin-top: 2rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)

#     st.subheader(f"{ticker} - {year} Quarterly Sentiment Trends")
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df["Quarter"], y=df["%Positive"], mode='lines+markers', name='%Positive', line=dict(color='green', width=3), marker=dict(size=10)))
#     fig.add_trace(go.Scatter(x=df["Quarter"], y=df["%Neutral"], mode='lines+markers', name='%Neutral', line=dict(color='gray', width=3, dash='dash'), marker=dict(size=10)))
#     fig.add_trace(go.Scatter(x=df["Quarter"], y=df["%Negative"], mode='lines+markers', name='%Negative', line=dict(color='red', width=3, dash='dot'), marker=dict(size=10)))
#     fig.update_layout(xaxis_title="Quarter", yaxis_title="Sentiment %", legend_title="Sentiment Type", template="plotly_dark", height=450)
#     st.plotly_chart(fig, use_container_width=True)

# st.markdown("---")

# #==============================================================================
# # BÖLÜM 2: İSTEK ÜZERİNE METİN ANALİZİ
# #==============================================================================

# st.header("Deep-Dive Sentiment Analysis")
# st.write("""
# Click the button to perform a deep-dive analysis on the backend's default MDA text using FinBERT.
# Results will be visualized below.
# """)

# if st.button("✨ Perform Deep-Dive Analysis"):
#     with st.spinner("Connecting to backend and running analysis... Please wait."):
#         try:
#             # API isteği aynı kalıyor
#             response = requests.get(DEFAULT_MDA_ANALYSIS_URL, timeout=300)
#             response.raise_for_status()

#             data = response.json()
#             results = data.get("sentiment_results")

#             st.success(f"Analysis Completed! Source: `{data.get('source', 'N/A')}`")
#             st.markdown("### Analysis Results")

#             # --- YENİ TASARIM BURADA BAŞLIYOR ---

#             # 1. Grafiğin verisini hazırla
#             labels = ['Positive Paragraphs', 'Negative Paragraphs', 'Neutral Paragraphs']
#             values = [
#                 results.get("count_positive_chunks", 0),
#                 results.get("count_negative_chunks", 0),
#                 results.get("count_neutral_chunks", 0)
#             ]
#             colors = ['#28a745', '#dc3545', '#6c757d'] # Yeşil, Kırmızı, Gri

#             # 2. Donut grafiğini oluştur
#             fig = go.Figure(data=[go.Pie(
#                 labels=labels,
#                 values=values,
#                 hole=.5, # Ortadaki delik için
#                 marker_colors=colors,
#                 pull=[0.05, 0, 0] # Pozitif dilimi biraz dışarı çıkar
#             )])

#             fig.update_layout(
#                 title_text="Paragraph Sentiment Distribution",
#                 template="plotly_dark",
#                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
#             )

#             # 3. Sonuçları iki sütun halinde göster
#             col1, col2 = st.columns([1, 1]) # Sütun genişlik oranları

#             with col1:
#                 # Sol sütuna grafiği koy
#                 st.plotly_chart(fig, use_container_width=True)

#             with col2:
#                 # Sağ sütuna en önemli metrikleri daha şık bir şekilde koy
#                 st.markdown("#### Key Metrics")

#                 st.markdown(f"""
#                 - **Peak Positive Score:** `{results.get("max_positive_score", 0):.4f}`
#                 - **Peak Negative Score:** `{results.get("max_negative_score", 0):.4f}`
#                 - **Average Positive Score:** `{results.get("avg_positive", 0):.4f}`
#                 - **Average Negative Score:** `{results.get("avg_negative", 0):.4f}`
#                 """)

#                 total_paragraphs = sum(values)
#                 st.info(f"A total of **{total_paragraphs}** paragraphs were analyzed.")

#             # Ham veriyi yine de bir expander içinde sunalım
#             with st.expander("View Raw Dictionary Output"):
#                 st.json(results)

#         except requests.exceptions.RequestException as e:
#             st.error(f"API Connection Error: Could not connect to the backend.")
#             st.info(f"Details: {e}")


import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
# Extractor API
from sec_api import ExtractorApi

# --- Sayfa Yapılandırması ve Başlık ---
st.set_page_config(page_title="Corporate Sentiment Analysis", layout="wide")
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Corporate Sentiment Analysis</h1>", unsafe_allow_html=True)

# --- Backend URL ---
DEFAULT_MDA_ANALYSIS_URL = "http://127.0.0.1:8000/analyze_default_mda/"

#==============================================================================
# BÖLÜM 1: ÇEYREK BAZLI TREND GÖSTERGE PANELİ
#==============================================================================
st.header("Quarterly Sentiment Trends (Dummy Data)")

# --- Veri Ayarları ---
company_db = {
    "JNJ": {"sector": "Healthcare", "years": [2022, 2023]},
    "PFE": {"sector": "Healthcare", "years": [2022, 2023]},
    "BA": {"sector": "Industrials", "years": [2022, 2023]},
    "CAT": {"sector": "Industrials", "years": [2022, 2023]},
    "MCD": {"sector": "Consumer Cyclical", "years": [2022, 2023]},
    "NKE": {"sector": "Consumer Cyclical", "years": [2022, 2023]},
    "AAPL": {"sector": "Technology", "years": [2021, 2022, 2023]},
    "MSFT": {"sector": "Technology", "years": [2021, 2022, 2023]},
    "PG": {"sector": "Consumer Defensive", "years": [2022, 2023]},
    "KO": {"sector": "Consumer Defensive", "years": [2022, 2023]},
    "NEE": {"sector": "Utilities", "years": [2022, 2023]},
    "DUK": {"sector": "Utilities", "years": [2022, 2023]},
    "JPM": {"sector": "Financial Services", "years": [2022, 2023]},
    "V": {"sector": "Financial Services", "years": [2022, 2023]},
    "PLD": {"sector": "Real Estate", "years": [2022, 2023]},
    "AMT": {"sector": "Real Estate", "years": [2022, 2023]},
    "XOM": {"sector": "Energy", "years": [2022, 2023]},
    "CVX": {"sector": "Energy", "years": [2022, 2023]},
    "GOOGL": {"sector": "Communication Services", "years": [2023, 2024]},
    "META": {"sector": "Communication Services", "years": [2023, 2024]},
    "TSLA": {"sector": "Consumer Discretionary", "years": [2022, 2023, 2024]},
    "AMZN": {"sector": "Consumer Discretionary", "years": [2023, 2024]},
    "LIN": {"sector": "Basic Materials", "years": [2022, 2023]}
}
sectors = sorted([
    "Healthcare", "Industrials", "Consumer Cyclical", "Technology",
    "Consumer Defensive", "Utilities", "Financial Services", "Real Estate",
    "Basic Materials", "Energy", "Communication Services",
    "Financials", "Materials", "Consumer Discretionary"
])
quarters = ["Q1", "Q2", "Q3", "Q4"]

@st.cache_data
def get_sentiment_data(ticker, year):
    np.random.seed(hash(f"{ticker}{year}") % (2**32 - 1))
    quarter_data = []
    for q in quarters:
        pos, neu = np.random.randint(40, 75), np.random.randint(10, 25)
        neg = 100 - pos - neu
        quarter_data.append({"Quarter": q, "%Positive": pos, "%Neutral": neu, "%Negative": neg})
    return pd.DataFrame(quarter_data)

# --- Filtreler ---
col1, col2, col3, col4 = st.columns(4)
with col2:
    selected_sector = st.selectbox("By Sector", sectors)
with col1:
    tickers_in_sector = [k for k, v in company_db.items() if v["sector"] == selected_sector]
    if not tickers_in_sector:
        st.warning(f"No sample tickers defined for {selected_sector}")
        ticker = None
    else:
        ticker = st.selectbox("By Ticker", tickers_in_sector)

if ticker:
    with col3:
        year = st.selectbox("By Year", company_db[ticker]["years"])
    with col4:
        timeframe = st.selectbox("Timeframe (Quarter)", quarters)

    st.markdown("---")

    # NAMEERROR DÜZELTMESİ: `df` değişkeni, kullanılmadan ÖNCE burada tanımlanıyor.
    df = get_sentiment_data(ticker, year)

    # Artık bu alt satırlar hata vermeyecektir.
    selected_row = df[df["Quarter"] == timeframe].iloc[0]
    colA, colB, colC, colD = st.columns(4)
    colA.metric("Quarter", timeframe)
    colB.metric("Positive (%)", f'{selected_row["%Positive"]:.0f}')
    colC.metric("Neutral (%)", f'{selected_row["%Neutral"]:.0f}')
    colD.metric("Negative (%)", f'{selected_row["%Negative"]:.0f}')

    st.markdown("<hr style='margin-top: 2rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)

    st.subheader(f"{ticker} - {year} Quarterly Sentiment Trends")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Quarter"], y=df["%Positive"], mode='lines+markers', name='%Positive', line=dict(color='green', width=3), marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=df["Quarter"], y=df["%Neutral"], mode='lines+markers', name='%Neutral', line=dict(color='gray', width=3, dash='dash'), marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=df["Quarter"], y=df["%Negative"], mode='lines+markers', name='%Negative', line=dict(color='red', width=3, dash='dot'), marker=dict(size=10)))
    fig.update_layout(xaxis_title="Quarter", yaxis_title="Sentiment %", legend_title="Sentiment Type", template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

#==============================================================================
# BÖLÜM 2: İSTEK ÜZERİNE METİN ANALİZİ (TEK VE NİHAİ VERSİYON)
#==============================================================================

st.header("Deep-Dive Sentiment Analysis")
st.write("""
Click the button to perform a deep-dive analysis on the backend's default MDA text using FinBERT.
Results will be visualized below.
""")

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



st.header("MDA Section Extraction from SEC API")

if st.button("✨get mda from sec api"):

    with st.spinner("Connecting to backend and running analysis... Please wait."):
        try:

            # Replace with your actual SEC-API key
            extractorApi = ExtractorApi(api_key="ac9ba652b06eae03d5f550d0585e3f9fdabaa36f186482b6f31f0d449514ff6b")

            #make it so that we get the mda we want (e.g. from a specific company and quarter)
            mda_file_api_test_url_10_q = "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000037996/000003799625000072/f-20250331.htm"

            mda_key_dict = {
                "10-Q": "part1item2",
                "10-K": "7"
            }

            #item 2 or 7 depending
            mdna_section = extractorApi.get_section(mda_file_api_test_url_10_q, mda_key_dict['10-Q'], "text")
            st.write(mdna_section)

        except Exception as e:
            st.error(f"API Connection Error: Could not connect to SEC API.")
            st.info(f"Details: {e}")
