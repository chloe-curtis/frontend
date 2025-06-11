import numpy as np
import pandas as pd

quarters = ["Q1", "Q2", "Q3", "Q4"]
#josh to fill with queried data
def get_sentiment_over_time(ticker_or_sector="AAPL"):

    """
        quarter _year
        ticker
        sector
        net_sentiment
    """

    data = {
        "quarter_year": [
            "2021_Q1", "2021_Q2", "2021_Q3", "2021_Q4",
            "2022_Q1", "2022_Q2", "2022_Q3", "2022_Q4",
            "2023_Q1", "2023_Q2", "2023_Q3", "2023_Q4"
        ],
        "ticker": ["AAPL"] * 12,
        "sector": ["Technology"] * 12,
        "net_sentiment": [0.10, 0.12, 0.08, 0.15, -0.05, 0.03, 0.06, 0.09, 0.14, 0.11, -0.02, 0.07]
    }

    df = pd.DataFrame(data)
    return df

def get_sentiment_data(ticker):
    np.random.seed(hash(f"{ticker}{2020}") % (2**32 - 1))
    quarter_data = []
    for q in quarters:
        pos, neu = np.random.randint(40, 75), np.random.randint(10, 25)
        neg = 100 - pos - neu
        quarter_data.append({"Quarter": q, "%Positive": pos, "%Neutral": neu, "%Negative": neg})

    return pd.DataFrame(quarter_data)
