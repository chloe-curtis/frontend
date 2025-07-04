import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from data_front import sector_sentiment, ticker_sentiment, TEST_MDA_TEXT
# from sec_api import ExtractorApi
from streamlit_extras.let_it_rain import rain

#glibal
call_sec_api = False
mdna_section = ""

# BACKEND_BASE_URL = "http://localhost:8000"
# BACKEND_BASE_URL = 'https://cst-217305741515.europe-west2.run.app/'
BACKEND_BASE_URL = 'https://corporate-sentiment-tracker-217305741515.europe-west1.run.app/'



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
#dont need?
sector_dict = {
    "A": {'sector': 'Healthcare'},
    "AAL": {'sector': 'Industrials'},
    "AAP": {'sector': 'Consumer Cyclical'},
    "AAPL": {'sector': 'Technology'},
    "ABBV": {'sector': 'Healthcare'},
    "ABC": {'sector': 'Healthcare'},
    "ABMD": {'sector': 'Healthcare'},
    "ABNB": {'sector': 'Consumer Cyclical'},
    "ABT": {'sector': 'Healthcare'},
    "ACGL": {'sector': 'Financial Services'},
    "ACN": {'sector': 'Technology'},
    "ADBE": {'sector': 'Technology'},
    "ADI": {'sector': 'Technology'},
    "ADM": {'sector': 'Consumer Defensive'},
    "ADP": {'sector': 'Technology'},
    "ADS": {'sector': 'Industrials'},
    "ADSK": {'sector': 'Technology'},
    "AEE": {'sector': 'Utilities'},
    "AEP": {'sector': 'Utilities'},
    "AES": {'sector': 'Utilities'},
    "AFL": {'sector': 'Financial Services'},
    "AGN": {'sector': 'Healthcare'},
    "AIG": {'sector': 'Financial Services'},
    "AIV": {'sector': 'Real Estate'},
    "AIZ": {'sector': 'Financial Services'},
    "AJG": {'sector': 'Financial Services'},
    "AKAM": {'sector': 'Technology'},
    "ALB": {'sector': 'Basic Materials'},
    "ALGN": {'sector': 'Healthcare'},
    "ALK": {'sector': 'Industrials'},
    "ALL": {'sector': 'Financial Services'},
    "ALLE": {'sector': 'Industrials'},
    "ALXN": {'sector': 'Healthcare'},
    "AMAT": {'sector': 'Technology'},
    "AMCR": {'sector': 'Consumer Cyclical'},
    "AMD": {'sector': 'Technology'},
    "AME": {'sector': 'Industrials'},
    "AMG": {'sector': 'Financial Services'},
    "AMGN": {'sector': 'Healthcare'},
    "AMP": {'sector': 'Financial Services'},
    "AMT": {'sector': 'Real Estate'},
    "AMTM": {'sector': 'Industrials'},
    "AMZN": {'sector': 'Consumer Cyclical'},
    "ANET": {'sector': 'Technology'},
    "ANSS": {'sector': 'Technology'},
    "ANTM": {'sector': 'Healthcare'},
    "AON": {'sector': 'Financial Services'},
    "AOS": {'sector': 'Industrials'},
    "APA": {'sector': 'Energy'},
    "APC": {'sector': 'Energy'},
    "APD": {'sector': 'Basic Materials'},
    "APH": {'sector': 'Technology'},
    "APTV": {'sector': 'Consumer Cyclical'},
    "ARE": {'sector': 'Real Estate'},
    "ARNC": {'sector': 'Industrials'},
    "ATO": {'sector': 'Utilities'},
    "ATVI": {'sector': 'Communication Services'},
    "AVB": {'sector': 'Real Estate'},
    "AVGO": {'sector': 'Technology'},
    "AVY": {'sector': 'Consumer Cyclical'},
    "AWK": {'sector': 'Utilities'},
    "AXON": {'sector': 'Industrials'},
    "AXP": {'sector': 'Financial Services'},
    "AZO": {'sector': 'Consumer Cyclical'},
    "BA": {'sector': 'Industrials'},
    "BAC": {'sector': 'Financial Services'},
    "BALL": {'sector': 'Consumer Cyclical'},
    "BAX": {'sector': 'Healthcare'},
    "BBWI": {'sector': 'Consumer Cyclical'},
    "BBY": {'sector': 'Consumer Cyclical'},
    "BDX": {'sector': 'Healthcare'},
    "BEN": {'sector': 'Financial Services'},
    "BF-B": {'sector': 'Consumer Defensive'},
    "BG": {'sector': 'Consumer Defensive'},
    "BHF": {'sector': 'Financial Services'},
    "BHGE": {'sector': 'Energy'},
    "BIIB": {'sector': 'Healthcare'},
    "BIO": {'sector': 'Healthcare'},
    "BK": {'sector': 'Financial Services'},
    "BKNG": {'sector': 'Consumer Cyclical'},
    "BKR": {'sector': 'Energy'},
    "BLDR": {'sector': 'Industrials'},
    "BLL": {'sector': 'Materials'},
    "BMY": {'sector': 'Healthcare'},
    "BR": {'sector': 'Technology'},
    "BRK-B": {'sector': 'Financial Services'},
    "BRO": {'sector': 'Financial Services'},
    "BSX": {'sector': 'Healthcare'},
    "BWA": {'sector': 'Consumer Cyclical'},
    "BX": {'sector': 'Financial Services'},
    "BXP": {'sector': 'Real Estate'},
    "CAG": {'sector': 'Consumer Defensive'},
    "CAH": {'sector': 'Healthcare'},
    "CARR": {'sector': 'Industrials'},
    "CAT": {'sector': 'Industrials'},
    "CB": {'sector': 'Financial Services'},
    "CBOE": {'sector': 'Financial Services'},
    "CBRE": {'sector': 'Real Estate'},
    "CBS": {'sector': 'Communication Services'},
    "CCI": {'sector': 'Real Estate'},
    "CCL": {'sector': 'Consumer Cyclical'},
    "CDAY": {'sector': 'Technology'},
    "CDNS": {'sector': 'Technology'},
    "CDW": {'sector': 'Technology'},
    "CE": {'sector': 'Basic Materials'},
    "CEG": {'sector': 'Utilities'},
    "CELG": {'sector': 'Healthcare'},
    "CERN": {'sector': 'Healthcare'},
    "CF": {'sector': 'Basic Materials'},
    "CFG": {'sector': 'Financial Services'},
    "CHD": {'sector': 'Consumer Defensive'},
    "CHRW": {'sector': 'Industrials'},
    "CHTR": {'sector': 'Communication Services'},
    "CI": {'sector': 'Healthcare'},
    "CINF": {'sector': 'Financial Services'},
    "CL": {'sector': 'Consumer Defensive'},
    "CLX": {'sector': 'Consumer Defensive'},
    "CMA": {'sector': 'Financial Services'},
    "CMCSA": {'sector': 'Communication Services'},
    "CME": {'sector': 'Financial Services'},
    "CMG": {'sector': 'Consumer Cyclical'},
    "CMI": {'sector': 'Industrials'},
    "CMS": {'sector': 'Utilities'},
    "CNC": {'sector': 'Healthcare'},
    "CNP": {'sector': 'Utilities'},
    "COF": {'sector': 'Financial Services'},
    "COG": {'sector': 'Energy'},
    "COO": {'sector': 'Healthcare'},
    "COP": {'sector': 'Energy'},
    "COR": {'sector': 'Healthcare'},
    "COST": {'sector': 'Consumer Defensive'},
    "COTY": {'sector': 'Consumer Defensive'},
    "CPAY": {'sector': 'Technology'},
    "CPB": {'sector': 'Consumer Defensive'},
    "CPRI": {'sector': 'Consumer Cyclical'},
    "CPRT": {'sector': 'Industrials'},
    "CPT": {'sector': 'Real Estate'},
    "CRL": {'sector': 'Healthcare'},
    "CRM": {'sector': 'Technology'},
    "CRWD": {'sector': 'Technology'},
    "CSCO": {'sector': 'Technology'},
    "CSGP": {'sector': 'Real Estate'},
    "CSX": {'sector': 'Industrials'},
    "CTAS": {'sector': 'Industrials'},
    "CTL": {'sector': 'Communication Services'},
    "CTLT": {'sector': 'Healthcare'},
    "CTRA": {'sector': 'Energy'},
    "CTSH": {'sector': 'Technology'},
    "CTVA": {'sector': 'Basic Materials'},
    "CTXS": {'sector': 'Technology'},
    "CVS": {'sector': 'Healthcare'},
    "CVX": {'sector': 'Energy'},
    "CXO": {'sector': 'Energy'},
    "CZR": {'sector': 'Consumer Cyclical'},
    "D": {'sector': 'Utilities'},
    "DAL": {'sector': 'Industrials'},
    "DAY": {'sector': 'Technology'},
    "DD": {'sector': 'Basic Materials'},
    "DE": {'sector': 'Industrials'},
    "DECK": {'sector': 'Consumer Cyclical'},
    "DELL": {'sector': 'Technology'},
    "DFS": {'sector': 'Financial Services'},
    "DG": {'sector': 'Consumer Defensive'},
    "DGX": {'sector': 'Healthcare'},
    "DHI": {'sector': 'Consumer Cyclical'},
    "DHR": {'sector': 'Healthcare'},
    "DIS": {'sector': 'Communication Services'},
    "DISCA": {'sector': 'Communication Services'},
    "DISCK": {'sector': 'Communication Services'},
    "DISH": {'sector': 'Communication Services'},
    "DLR": {'sector': 'Real Estate'},
    "DLTR": {'sector': 'Consumer Defensive'},
    "DOC": {'sector': 'Real Estate'},
    "DOV": {'sector': 'Industrials'},
    "DOW": {'sector': 'Basic Materials'},
    "DPZ": {'sector': 'Consumer Cyclical'},
    "DRE": {'sector': 'Real Estate'},
    "DRI": {'sector': 'Consumer Cyclical'},
    "DTE": {'sector': 'Utilities'},
    "DUK": {'sector': 'Utilities'},
    "DVA": {'sector': 'Healthcare'},
    "DVN": {'sector': 'Energy'},
    "DWDP": {'sector': 'Materials'},
    "DXC": {'sector': 'Technology'},
    "DXCM": {'sector': 'Healthcare'},
    "EA": {'sector': 'Communication Services'},
    "EBAY": {'sector': 'Consumer Cyclical'},
    "ECL": {'sector': 'Basic Materials'},
    "ED": {'sector': 'Utilities'},
    "EFX": {'sector': 'Industrials'},
    "EG": {'sector': 'Financial Services'},
    "EL": {'sector': 'Consumer Defensive'},
    "ELV": {'sector': 'Healthcare'},
    "EMN": {'sector': 'Basic Materials'},
    "ENPH": {'sector': 'Technology'},
    "EOG": {'sector': 'Energy'},
    "EPAM": {'sector': 'Technology'},
    "EQIX": {'sector': 'Real Estate'},
    "EQR": {'sector': 'Real Estate'},
    "EQT": {'sector': 'Energy'},
    "ERIE": {'sector': 'Financial Services'},
    "ES": {'sector': 'Utilities'},
    "ESS": {'sector': 'Real Estate'},
    "ETFC": {'sector': 'Financials'},
    "ETN": {'sector': 'Industrials'},
    "ETR": {'sector': 'Utilities'},
    "ETSY": {'sector': 'Consumer Cyclical'},
    "EVRG": {'sector': 'Utilities'},
    "EW": {'sector': 'Healthcare'},
    "EXC": {'sector': 'Utilities'},
    "EXPD": {'sector': 'Industrials'},
    "EXPE": {'sector': 'Consumer Cyclical'},
    "EXR": {'sector': 'Real Estate'},
    "F": {'sector': 'Consumer Cyclical'},
    "FANG": {'sector': 'Energy'},
    "FAST": {'sector': 'Industrials'},
    "FB": {'sector': 'Communication Services'},
    "FBHS": {'sector': 'Consumer Discretionary'},
    "FCX": {'sector': 'Basic Materials'},
    "FDS": {'sector': 'Financial Services'},
    "FDX": {'sector': 'Industrials'},
    "FE": {'sector': 'Utilities'},
    "FFIV": {'sector': 'Technology'},
    "FI": {'sector': 'Technology'},
    "FICO": {'sector': 'Technology'},
    "FIS": {'sector': 'Technology'},
    "FISV": {'sector': 'Technology'},
    "FITB": {'sector': 'Financial Services'},
    "FL": {'sector': 'Consumer Cyclical'},
    "FLIR": {'sector': 'Industrials'},
    "FLR": {'sector': 'Industrials'},
    "FLS": {'sector': 'Industrials'},
    "FLT": {'sector': 'Industrials'},
    "FMC": {'sector': 'Basic Materials'},
    "FOX": {'sector': 'Communication Services'},
    "FOXA": {'sector': 'Communication Services'},
    "FRT": {'sector': 'Real Estate'},
    "FSLR": {'sector': 'Technology'},
    "FTI": {'sector': 'Energy'},
    "FTNT": {'sector': 'Technology'},
    "FTV": {'sector': 'Technology'},
    "GD": {'sector': 'Industrials'},
    "GDDY": {'sector': 'Technology'},
    "GE": {'sector': 'Industrials'},
    "GEHC": {'sector': 'Healthcare'},
    "GEN": {'sector': 'Technology'},
    "GEV": {'sector': 'Industrials'},
    "GILD": {'sector': 'Healthcare'},
    "GIS": {'sector': 'Consumer Defensive'},
    "GL": {'sector': 'Financial Services'},
    "GLW": {'sector': 'Technology'},
    "GM": {'sector': 'Consumer Cyclical'},
    "GNRC": {'sector': 'Industrials'},
    "GOOG": {'sector': 'Communication Services'},
    "GOOGL": {'sector': 'Communication Services'},
    "GPC": {'sector': 'Consumer Cyclical'},
    "GPN": {'sector': 'Industrials'},
    "GPS": {'sector': 'Consumer Discretionary'},
    "GRMN": {'sector': 'Technology'},
    "GS": {'sector': 'Financial Services'},
    "GWW": {'sector': 'Industrials'},
    "HAL": {'sector': 'Energy'},
    "HAS": {'sector': 'Consumer Cyclical'},
    "HBI": {'sector': 'Consumer Cyclical'},
    "HCA": {'sector': 'Healthcare'},
    "HCP": {'sector': 'Real Estate'},
    "HD": {'sector': 'Consumer Cyclical'},
    "HES": {'sector': 'Energy'},
    "HFC": {'sector': 'Energy'},
    "HII": {'sector': 'Industrials'},
    "HLT": {'sector': 'Consumer Cyclical'},
    "HOG": {'sector': 'Consumer Cyclical'},
    "HOLX": {'sector': 'Healthcare'},
    "HON": {'sector': 'Industrials'},
    "HP": {'sector': 'Energy'},
    "HPE": {'sector': 'Technology'},
    "HPQ": {'sector': 'Technology'},
    "HRB": {'sector': 'Consumer Cyclical'},
    "HRL": {'sector': 'Consumer Defensive'},
    "HSIC": {'sector': 'Healthcare'},
    "HST": {'sector': 'Real Estate'},
    "HSY": {'sector': 'Consumer Defensive'},
    "HUBB": {'sector': 'Industrials'},
    "HUM": {'sector': 'Healthcare'},
    "HWM": {'sector': 'Industrials'},
    "IBM": {'sector': 'Technology'},
    "ICE": {'sector': 'Financial Services'},
    "IDXX": {'sector': 'Healthcare'},
    "IEX": {'sector': 'Industrials'},
    "IFF": {'sector': 'Basic Materials'},
    "ILMN": {'sector': 'Healthcare'},
    "INCY": {'sector': 'Healthcare'},
    "INFO": {'sector': 'Technology'},
    "INTC": {'sector': 'Technology'},
    "INTU": {'sector': 'Technology'},
    "INVH": {'sector': 'Real Estate'},
    "IP": {'sector': 'Consumer Cyclical'},
    "IPG": {'sector': 'Communication Services'},
    "IPGP": {'sector': 'Technology'},
    "IQV": {'sector': 'Healthcare'},
    "IR": {'sector': 'Industrials'},
    "IRM": {'sector': 'Real Estate'},
    "ISRG": {'sector': 'Healthcare'},
    "IT": {'sector': 'Technology'},
    "ITW": {'sector': 'Industrials'},
    "IVZ": {'sector': 'Financial Services'},
    "J": {'sector': 'Industrials'},
    "JBHT": {'sector': 'Industrials'},
    "JBL": {'sector': 'Technology'},
    "JCI": {'sector': 'Industrials'},
    "JEC": {'sector': 'Industrials'},
    "JEF": {'sector': 'Financial Services'},
    "JKHY": {'sector': 'Technology'},
    "JNJ": {'sector': 'Healthcare'},
    "JNPR": {'sector': 'Technology'},
    "JPM": {'sector': 'Financial Services'},
    "JWN": {'sector': 'Consumer Cyclical'},
    "K": {'sector': 'Consumer Defensive'},
    "KDP": {'sector': 'Consumer Defensive'},
    "KEY": {'sector': 'Financial Services'},
    "KEYS": {'sector': 'Technology'},
    "KHC": {'sector': 'Consumer Defensive'},
    "KIM": {'sector': 'Real Estate'},
    "KKR": {'sector': 'Financial Services'},
    "KLAC": {'sector': 'Technology'},
    "KMB": {'sector': 'Consumer Defensive'},
    "KMI": {'sector': 'Energy'},
    "KMX": {'sector': 'Consumer Cyclical'},
    "KO": {'sector': 'Consumer Defensive'},
    "KR": {'sector': 'Consumer Defensive'},
    "KSS": {'sector': 'Consumer Cyclical'},
    "KSU": {'sector': 'Industrials'},
    "KVUE": {'sector': 'Consumer Defensive'},
    "L": {'sector': 'Financial Services'},
    "LDOS": {'sector': 'Technology'},
    "LEG": {'sector': 'Consumer Cyclical'},
    "LEN": {'sector': 'Consumer Cyclical'},
    "LH": {'sector': 'Healthcare'},
    "LHX": {'sector': 'Industrials'},
    "LIN": {'sector': 'Basic Materials'},
    "LKQ": {'sector': 'Consumer Cyclical'},
    "LLY": {'sector': 'Healthcare'},
    "LMT": {'sector': 'Industrials'},
    "LNC": {'sector': 'Financial Services'},
    "LNT": {'sector': 'Utilities'},
    "LOW": {'sector': 'Consumer Cyclical'},
    "LRCX": {'sector': 'Technology'},
    "LULU": {'sector': 'Consumer Cyclical'},
    "LUMN": {'sector': 'Communication Services'},
    "LUV": {'sector': 'Industrials'},
    "LVS": {'sector': 'Consumer Cyclical'},
    "LW": {'sector': 'Consumer Defensive'},
    "LYB": {'sector': 'Basic Materials'},
    "LYV": {'sector': 'Communication Services'},
    "M": {'sector': 'Consumer Cyclical'},
    "MA": {'sector': 'Financial Services'},
    "MAA": {'sector': 'Real Estate'},
    "MAC": {'sector': 'Real Estate'},
    "MAR": {'sector': 'Consumer Cyclical'},
    "MAS": {'sector': 'Industrials'},
    "MAT": {'sector': 'Consumer Cyclical'},
    "MCD": {'sector': 'Consumer Cyclical'},
    "MCHP": {'sector': 'Technology'},
    "MCK": {'sector': 'Healthcare'},
    "MCO": {'sector': 'Financial Services'},
    "MDLZ": {'sector': 'Consumer Defensive'},
    "MDT": {'sector': 'Healthcare'},
    "MET": {'sector': 'Financial Services'},
    "META": {'sector': 'Communication Services'},
    "MGM": {'sector': 'Consumer Cyclical'},
    "MHK": {'sector': 'Consumer Cyclical'},
    "MKC": {'sector': 'Consumer Defensive'},
    "MKTX": {'sector': 'Financial Services'},
    "MLM": {'sector': 'Basic Materials'},
    "MMC": {'sector': 'Financial Services'},
    "MMM": {'sector': 'Industrials'},
    "MNST": {'sector': 'Consumer Defensive'},
    "MO": {'sector': 'Consumer Defensive'},
    "MOS": {'sector': 'Basic Materials'},
    "MPC": {'sector': 'Energy'},
    "MPWR": {'sector': 'Technology'},
    "MRK": {'sector': 'Healthcare'},
    "MRNA": {'sector': 'Healthcare'},
    "MRO": {'sector': 'Energy'},
    "MSCI": {'sector': 'Financial Services'},
    "MSFT": {'sector': 'Technology'},
    "MSI": {'sector': 'Technology'},
    "MTB": {'sector': 'Financial Services'},
    "MTCH": {'sector': 'Communication Services'},
    "MTD": {'sector': 'Healthcare'},
    "MU": {'sector': 'Technology'},
    "MXIM": {'sector': 'Technology'},
    "MYL": {'sector': 'Healthcare'},
    "NBL": {'sector': 'Energy'},
    "NCLH": {'sector': 'Consumer Cyclical'},
    "NDAQ": {'sector': 'Financial Services'},
    "NDSN": {'sector': 'Industrials'},
    "NEE": {'sector': 'Utilities'},
    "NEM": {'sector': 'Basic Materials'},
    "NFLX": {'sector': 'Communication Services'},
    "NI": {'sector': 'Utilities'},
    "NKE": {'sector': 'Consumer Cyclical'},
    "NKTR": {'sector': 'Healthcare'},
    "NLOK": {'sector': 'Technology'},
    "NLSN": {'sector': 'Industrials'},
    "NOC": {'sector': 'Industrials'},
    "NOV": {'sector': 'Energy'},
    "NOW": {'sector': 'Technology'},
    "NRG": {'sector': 'Utilities'},
    "NSC": {'sector': 'Industrials'},
    "NTAP": {'sector': 'Technology'},
    "NTRS": {'sector': 'Financial Services'},
    "NUE": {'sector': 'Basic Materials'},
    "NVDA": {'sector': 'Technology'},
    "NVR": {'sector': 'Consumer Cyclical'},
    "NWL": {'sector': 'Consumer Defensive'},
    "NWS": {'sector': 'Communication Services'},
    "NWSA": {'sector': 'Communication Services'},
    "NXPI": {'sector': 'Technology'},
    "O": {'sector': 'Real Estate'},
    "ODFL": {'sector': 'Industrials'},
    "OGN": {'sector': 'Healthcare'},
    "OKE": {'sector': 'Energy'},
    "OMC": {'sector': 'Communication Services'},
    "ON": {'sector': 'Technology'},
    "ORCL": {'sector': 'Technology'},
    "ORLY": {'sector': 'Consumer Cyclical'},
    "OTIS": {'sector': 'Industrials'},
    "OXY": {'sector': 'Energy'},
    "PANW": {'sector': 'Technology'},
    "PARA": {'sector': 'Communication Services'},
    "PAYC": {'sector': 'Technology'},
    "PBCT": {'sector': 'Financials'},
    "PCAR": {'sector': 'Industrials'},
    "PCG": {'sector': 'Utilities'},
    "PEAK": {'sector': 'Real Estate'},
    "PEG": {'sector': 'Utilities'},
    "PENN": {'sector': 'Consumer Cyclical'},
    "PEP": {'sector': 'Consumer Defensive'},
    "PFE": {'sector': 'Healthcare'},
    "PFG": {'sector': 'Financial Services'},
    "PG": {'sector': 'Consumer Defensive'},
    "PGR": {'sector': 'Financial Services'},
    "PH": {'sector': 'Industrials'},
    "PHM": {'sector': 'Consumer Cyclical'},
    "PKG": {'sector': 'Consumer Cyclical'},
    "PKI": {'sector': 'Healthcare'},
    "PLD": {'sector': 'Real Estate'},
    "PLTR": {'sector': 'Technology'},
    "PM": {'sector': 'Consumer Defensive'},
    "PNC": {'sector': 'Financial Services'},
    "PNR": {'sector': 'Industrials'},
    "PNW": {'sector': 'Utilities'},
    "PODD": {'sector': 'Healthcare'},
    "POOL": {'sector': 'Industrials'},
    "PPG": {'sector': 'Basic Materials'},
    "PPL": {'sector': 'Utilities'},
    "PRGO": {'sector': 'Healthcare'},
    "PRU": {'sector': 'Financial Services'},
    "PSA": {'sector': 'Real Estate'},
    "PSX": {'sector': 'Energy'},
    "PTC": {'sector': 'Technology'},
    "PVH": {'sector': 'Consumer Cyclical'},
    "PWR": {'sector': 'Industrials'},
    "PXD": {'sector': 'Energy'},
    "PYPL": {'sector': 'Financial Services'},
    "QCOM": {'sector': 'Technology'},
    "QRVO": {'sector': 'Technology'},
    "RCL": {'sector': 'Consumer Cyclical'},
    "RE": {'sector': 'Financials'},
    "REG": {'sector': 'Real Estate'},
    "REGN": {'sector': 'Healthcare'},
    "RF": {'sector': 'Financial Services'},
    "RHI": {'sector': 'Industrials'},
    "RHT": {'sector': 'Technology'},
    "RJF": {'sector': 'Financial Services'},
    "RL": {'sector': 'Consumer Cyclical'},
    "RMD": {'sector': 'Healthcare'},
    "ROK": {'sector': 'Industrials'},
    "ROL": {'sector': 'Consumer Cyclical'},
    "ROP": {'sector': 'Technology'},
    "ROST": {'sector': 'Consumer Cyclical'},
    "RSG": {'sector': 'Industrials'},
    "RTN": {'sector': 'Industrials'},
    "RTX": {'sector': 'Industrials'},
    "RVTY": {'sector': 'Healthcare'},
    "SBAC": {'sector': 'Real Estate'},
    "SBUX": {'sector': 'Consumer Cyclical'},
    "SCHW": {'sector': 'Financial Services'},
    "SEDG": {'sector': 'Technology'},
    "SEE": {'sector': 'Consumer Cyclical'},
    "SHW": {'sector': 'Basic Materials'},
    "SIVB": {'sector': 'Financials'},
    "SJM": {'sector': 'Consumer Defensive'},
    "SLB": {'sector': 'Energy'},
    "SLG": {'sector': 'Real Estate'},
    "SMCI": {'sector': 'Technology'},
    "SNA": {'sector': 'Industrials'},
    "SNPS": {'sector': 'Technology'},
    "SO": {'sector': 'Utilities'},
    "SOLV": {'sector': 'Healthcare'},
    "SPG": {'sector': 'Real Estate'},
    "SPGI": {'sector': 'Financial Services'},
    "SRE": {'sector': 'Utilities'},
    "STE": {'sector': 'Healthcare'},
    "STLD": {'sector': 'Basic Materials'},
    "STT": {'sector': 'Financial Services'},
    "STX": {'sector': 'Technology'},
    "STZ": {'sector': 'Consumer Defensive'},
    "SW": {'sector': 'Consumer Cyclical'},
    "SWK": {'sector': 'Industrials'},
    "SWKS": {'sector': 'Technology'},
    "SYF": {'sector': 'Financial Services'},
    "SYK": {'sector': 'Healthcare'},
    "SYMC": {'sector': 'Technology'},
    "SYY": {'sector': 'Consumer Defensive'},
    "T": {'sector': 'Communication Services'},
    "TAP": {'sector': 'Consumer Defensive'},
    "TDG": {'sector': 'Industrials'},
    "TDY": {'sector': 'Technology'},
    "TECH": {'sector': 'Healthcare'},
    "TEL": {'sector': 'Technology'},
    "TER": {'sector': 'Technology'},
    "TFC": {'sector': 'Financial Services'},
    "TFX": {'sector': 'Healthcare'},
    "TGT": {'sector': 'Consumer Defensive'},
    "TIF": {'sector': 'Consumer Discretionary'},
    "TJX": {'sector': 'Consumer Cyclical'},
    "TMK": {'sector': 'Financials'},
    "TMO": {'sector': 'Healthcare'},
    "TMUS": {'sector': 'Communication Services'},
    "TPR": {'sector': 'Consumer Cyclical'},
    "TRGP": {'sector': 'Energy'},
    "TRIP": {'sector': 'Consumer Cyclical'},
    "TRMB": {'sector': 'Technology'},
    "TROW": {'sector': 'Financial Services'},
    "TRV": {'sector': 'Financial Services'},
    "TSCO": {'sector': 'Consumer Cyclical'},
    "TSLA": {'sector': 'Consumer Cyclical'},
    "TSN": {'sector': 'Consumer Defensive'},
    "TT": {'sector': 'Industrials'},
    "TTWO": {'sector': 'Communication Services'},
    "TWTR": {'sector': 'Communication Services'},
    "TXN": {'sector': 'Technology'},
    "TXT": {'sector': 'Industrials'},
    "TYL": {'sector': 'Technology'},
    "UA": {'sector': 'Consumer Cyclical'},
    "UAA": {'sector': 'Consumer Cyclical'},
    "UAL": {'sector': 'Industrials'},
    "UBER": {'sector': 'Technology'},
    "UDR": {'sector': 'Real Estate'},
    "UHS": {'sector': 'Healthcare'},
    "ULTA": {'sector': 'Consumer Cyclical'},
    "UNH": {'sector': 'Healthcare'},
    "UNM": {'sector': 'Financial Services'},
    "UNP": {'sector': 'Industrials'},
    "UPS": {'sector': 'Industrials'},
    "URI": {'sector': 'Industrials'},
    "USB": {'sector': 'Financial Services'},
    "UTX": {'sector': 'Industrials'},
    "V": {'sector': 'Financial Services'},
    "VAR": {'sector': 'Healthcare'},
    "VFC": {'sector': 'Consumer Cyclical'},
    "VIAB": {'sector': 'Communication Services'},
    "VICI": {'sector': 'Real Estate'},
    "VLO": {'sector': 'Energy'},
    "VLTO": {'sector': 'Industrials'},
    "VMC": {'sector': 'Basic Materials'},
    "VNO": {'sector': 'Real Estate'},
    "VNT": {'sector': 'Technology'},
    "VRSK": {'sector': 'Industrials'},
    "VRSN": {'sector': 'Technology'},
    "VRTX": {'sector': 'Healthcare'},
    "VST": {'sector': 'Utilities'},
    "VTR": {'sector': 'Real Estate'},
    "VTRS": {'sector': 'Healthcare'},
    "VZ": {'sector': 'Communication Services'},
    "WAB": {'sector': 'Industrials'},
    "WAT": {'sector': 'Healthcare'},
    "WBA": {'sector': 'Healthcare'},
    "WBD": {'sector': 'Communication Services'},
    "WCG": {'sector': 'Healthcare'},
    "WDAY": {'sector': 'Technology'},
    "WDC": {'sector': 'Technology'},
    "WEC": {'sector': 'Utilities'},
    "WELL": {'sector': 'Real Estate'},
    "WFC": {'sector': 'Financial Services'},
    "WHR": {'sector': 'Consumer Cyclical'},
    "WLTW": {'sector': 'Financials'},
    "WM": {'sector': 'Industrials'},
    "WMB": {'sector': 'Energy'},
    "WMT": {'sector': 'Consumer Defensive'},
    "WRB": {'sector': 'Financial Services'},
    "WRK": {'sector': 'Materials'},
    "WST": {'sector': 'Healthcare'},
    "WTW": {'sector': 'Financial Services'},
    "WU": {'sector': 'Financial Services'},
    "WY": {'sector': 'Real Estate'},
    "WYNN": {'sector': 'Consumer Cyclical'},
    "XEC": {'sector': 'Energy'},
    "XEL": {'sector': 'Utilities'},
    "XLNX": {'sector': 'Technology'},
    "XOM": {'sector': 'Energy'},
    "XRAY": {'sector': 'Healthcare'},
    "XRX": {'sector': 'Technology'},
    "XYL": {'sector': 'Industrials'},
    "YUM": {'sector': 'Consumer Cyclical'},
    "ZBH": {'sector': 'Healthcare'},
    "ZBRA": {'sector': 'Technology'},
    "ZION": {'sector': 'Financial Services'},
    "ZTS": {'sector': 'Healthcare'},
}

url_db = {
    "BBY": {
        'html' : 'https://www.sec.gov/Archives/edgar/data/764478/000076447825000019/bby-20250503x10q.htm',
        'mda': """We are driven by our purpose to enrich lives through technology and our vision to personalize and humanize technology solutions for every stage of life. We accomplish this by leveraging our combination of tech expertise and a human touch to meet our customers’ everyday needs, whether they come to us online, visit our stores or invite us into their homes.
                We have two reportable segments: Domestic and International. The Domestic segment is comprised of our operations in all states, districts and territories of the U.S. and our Best Buy Health business. The International segment is comprised of all our operations in Canada.
                Our fiscal year ends on the Saturday nearest the end of January. Our business, like that of many retailers, is seasonal. A large proportion of our revenue and earnings is generated in the fiscal fourth quarter, which includes the majority of the holiday shopping season.
            """,
        'neutral_dominance': 'FALSE',
        'net_sentiment': -0.45,
        'up_and_down': 'DOWN'
    },
    "TSLA" : {
        "html" : 'https://www.sec.gov/ix?doc=/Archives/edgar/data/0001318605/000162828025018911/tsla-20250331.htm',
        'mda': """Our mission is to accelerate the world’s transition to sustainable energy. We design, develop, manufacture, lease and sell high-performance fully electric vehicles, solar energy generation systems and energy storage products. We also offer maintenance, installation, operation, charging, insurance, financial and other services related to our products. Additionally, we are increasingly focused on products and services based on AI, robotics and automation.
	As a result of rapidly evolving trade policy, uncertainty in the automotive and energy markets continues to increase, posing risks to our global supply chain and cost structure which could have a meaningfully adverse impact on demand for our products and our profitability. The current tariff regime will have a relatively larger impact on our energy generation and storage business compared to our automotive business. While we prepare for near-term challenges to our business under current policies, we are focused on long-term growth opportunities as we continue to make prudent investments.""",
        'neutral_dominance': 'FALSE',
        'net_sentiment': 0.15,
        'up_and_down': 'UP'
    },
    "LYV": {
        "html" : 'https://www.sec.gov/ix?doc=/Archives/edgar/data/0001335258/000133525825000055/lyv-20250331.htm',
        'mda': """
        The first quarter was a strong start to the year for the Company with one of our highest operating income and adjusted operating income results ever for the first quarter. Based on our strong pipeline of stadium shows for the remainder of the year, coupled with our current deferred revenue balance of $6.1 billion as of March 31, 2025, which is up $1.1 billion or 21% compared to March 31, 2024, we are optimistic for continued success in the remainder of the year.
	    Our overall revenue decreased by 11% to $3.4 billion on a reported basis, or 8% decline on a constant currency basis as compared to the same period of the prior year. This was largely the result of a reduction in arena show volume in the United States. Despite this, our operating income for the quarter increased by $156.2 million, from an operating loss of $41.4 million in the first quarter of 2024 to an operating income of $114.8 million in the first quarter of 2025 due to higher operating performance from our Concerts and Sponsorship segments as well as the Astroworld estimated loss contingencies recorded in our Concerts segment in the first quarter of 2024. The increase in operating income was $170.9 million at constant currency.
        """,
        'neutral_dominance': 'TRUE',
        'net_sentiment': -0.2,
        'up_and_down': 'DOWN'
    }
}

all_tickers = list(company_db.keys())
all_sectors = sorted(set([v["sector"] for v in company_db.values()]))

ticker_names = [f"{company_db[t]['name']} ({t.upper()})" for t in all_tickers]
ticker_label_to_ticker = {f"{company_db[t]['name']} ({t.upper()})": t for t in all_tickers}

selected_ticker = st.selectbox("Select Ticker", all_tickers)

net_sentiment_df = ticker_sentiment(selected_ticker)

# --- Show full DataFrame ---
st.markdown("---")
st.subheader("All Quarters Table")
st.dataframe(net_sentiment_df, use_container_width=True)
### josh comment out old code######
# if net_sentiment_df.empty:
#     st.warning("No data available for the selected ticker.")
#     st.stop()

# --- 5. Modern Bar Chart (Up Green / Down Red) ---
st.subheader("Quarterly Net Sentiment (Bar Chart)")
colors = ["#00CC96" if val >= 0 else "#EF553B" for val in net_sentiment_df["net_sentiment"]]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=net_sentiment_df["quarter_year"],
    y=net_sentiment_df["net_sentiment"],
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

# --- Quarter-Year Selectbox ---
quarter_year_options = net_sentiment_df["quarter_year"].dropna().unique()
quarter_year_options.sort()
selected_quarter = st.selectbox("Select Quarter & Year", quarter_year_options)

# --- Filter the selected row ---
row = net_sentiment_df[net_sentiment_df["quarter_year"] == selected_quarter]

if row.empty:
    st.warning("No data for the selected quarter.")
    st.stop()

selected_row = row.iloc[0]

# --- Display metrics ---
colA, colB, colC, colD = st.columns(4)
colA.metric("Quarter-Year", str(selected_row["quarter_year"]))
colB.metric("Net Sentiment", f'{selected_row["net_sentiment"]:.2f}')
colC.metric("Sector", str(selected_row["sector"]))
colD.metric("Ticker", str(selected_row["ticker"]))

st.markdown("---")

# Streamlit UI
st.header("MDA Section Extraction from SEC URL, by ticker")

all_urls = list(url_db.keys())
selected_url = st.selectbox("Select Ticker", all_urls)

data = url_db[selected_url]
mda = data.get('mda', 'No MDA data available')
response = requests.get(data['html'])
# Display all data
st.markdown(f"**MDA Section:** {data.get('mda', 'No data')}")
# st.markdown(f"**Neutral Dominance:** {data.get('neutral_dominance', 'N/A')}")
# st.markdown(f"**Net Sentiment:** {data.get('net_sentiment', 'N/A')}")
# st.markdown(f"\n**Prediction:** {data.get('up_and_down', 'N/A')}")


st.markdown("---")

def example():
    rain(
        emoji="💵",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )


# --- Make prediction from MDA section ---
prediction_endpoint = f"{BACKEND_BASE_URL}/get_prediction_from_mda"

if st.button("✨ Get Prediction from MDA"):
    with st.spinner("Getting prediction from backend..."):
        try:
            mda_text = data.get('mda', '')

            response = requests.post(
                prediction_endpoint,
                json={"mda_payload": mda_text, 'selected_ticker': selected_url},
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            prediction = result.get("prediction", "No prediction returned")
            neutral_dominance = result.get("neutral_dominance", "N/A")
            net_sentiment = result.get("net_sentiment", "N/A")
            # sentiment_entropy = result.get("sentiment_entropy", "N/A")
            st.success(f"Prediction: {'Stock Price will likely to go up!' if prediction==1 else 'Stock Price will likely to go down...'}")
            st.success(f"Neutral Dominance: {neutral_dominance}")
            st.success(f"Net Sentiment: {round(net_sentiment, 4)}")
            if prediction == 1:
                rain('💵')

            # st.success(f"Sentiment Entropy: {sentiment_entropy}")
        except Exception as e:
            st.error(f"Error getting prediction: {e}")

st.markdown("---")
