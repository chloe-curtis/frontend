import numpy as np
import pandas as pd
from google.cloud import bigquery
from data_utils_front import download_df_from_bq


# Initialize BigQuery client
# client = bigquery.Client()

# def get_all_net_sentiment():
#     # Define your table path
#     # net_sentiment = "sentiment-lewagon.sentiment_db.net_sentiment"
#     # ns = client.list_rows(net_sentiment).to_dataframe()
#     custom_query = """"""
#     ns = download_df_from_bq("net_sentiment", custom_query=custom_query)
#     ns = ns[ns['quarter_year'] != 'Q4-24']

#     # Function to convert 'Q1-21' to '2021_Q1'
#     def convert_quarter_format(q):
#         quarter, year_suffix = q.split('-')
#         year_prefix = '20' + year_suffix  # e.g., '21' -> '2021'
#         return f"{year_prefix}_{quarter}"

#     # Apply the function to the column
#     ns['quarter_year'] = ns['quarter_year'].apply(convert_quarter_format)

#     return ns

def convert_quarter_format(q):
        # e.g., 'Q4-24' -> 2023_Q3
        quarter, year_suffix = q.split('-')
        year_prefix = '20' + year_suffix 
        return f"{year_prefix}_{quarter}"

def ticker_sentiment(ticker):
    query_ticker = f"""
        SELECT quarter_year, ticker, sector, net_sentiment FROM `sentiment-lewagon.sentiment_db.net_sentiment`
        WHERE 
            quarter_year != 'Q4-24'
                AND 
            ticker = '{ticker}'
        """
    ticker_df = download_df_from_bq("net_sentiment", custom_query=query_ticker)

    # Apply the function to the column
    ticker_df['quarter_year'] = ticker_df['quarter_year'].apply(convert_quarter_format)

    return ticker_df.sort_values(by='quarter_year', ascending=True)

def sector_sentiment(sector):
    query_sector = f"""
        SELECT quarter_year, sector, avg(net_sentiment) as net_sentiment
        FROM `sentiment-lewagon.sentiment_db.net_sentiment`
        WHERE quarter_year != 'Q4-24'
        AND sector = '{sector}'
        GROUP BY quarter_year, sector
        """
    sector_df = download_df_from_bq("net_sentiment", custom_query=query_sector)

    # Apply the function to the column
    sector_df['quarter_year'] = sector_df['quarter_year'].apply(convert_quarter_format)

    return sector_df.sort_values(by='quarter_year', ascending=True)

###### OLD CODE BELOW, CAN WE DELETE?

# quarters = ["Q1", "Q2", "Q3", "Q4"]
# #josh to fill with queried data
# def get_sentiment_over_time_placeholder(df, ticker=None):
#     """
#         ticker
#         sector
#     """
#         ns = get_all_net_sentiment()
#     # Enforce that only one of ticker or sector is provided

#     data = {
#         "quarter_year": [
#             "2021_Q1", "2021_Q2", "2021_Q3", "2021_Q4",
#             "2022_Q1", "2022_Q2", "2022_Q3", "2022_Q4",
#             "2023_Q1", "2023_Q2", "2023_Q3", "2023_Q4",
#             "2024_Q1", "2024_Q2", "2024_Q3", "2024_Q4"
#         ],
#         "ticker": [ticker] * 16 if ticker else [None] * 16,
#         "sector": [sector] * 16 if sector else [None] * 16,
#         "net_sentiment": net_sentiment
#     }
#     df = pd.DataFrame(data)
#     return df

#  def get_sentiment_over_time(df, sector=None):
#     # Filter by sector if provided
#     if sector is not None:
#         df = df[df['sector'] == sector]

#     # Group by sector and compute average net sentiment
#     grouped = df.groupby('sector', as_index=False).agg({
#         'net_sentiment': 'mean',
#         # Add more aggregations if needed
#     })

#     grouped = ns[['quarter _year'
#         'ticker'
#         'sector'
#         'net_sentiment']]
#     return grouped



# def get_sentiment_data(ticker):
#     np.random.seed(hash(f"{ticker}{2020}") % (2**32 - 1))
#     quarter_data = []
#     for q in quarters:
#         pos, neu = np.random.randint(40, 75), np.random.randint(10, 25)
#         neg = 100 - pos - neu
#         quarter_data.append({"Quarter": q, "%Positive": pos, "%Neutral": neu, "%Negative": neg})

#     return pd.DataFrame(quarter_data)
