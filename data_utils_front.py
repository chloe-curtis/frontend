#data_helpers.py
#functions to download/upload to BQ
#functions to get text from bucket
# from data_utils import get_mda_from_text
#bucket
from google.cloud import storage
from google.api_core.exceptions import NotFound
# big query
from google.cloud import bigquery

#bq access from streamlit
from google.oauth2 import service_account
from google.cloud import bigquery
import streamlit as st

import re

BQ_PROJECT_ID = 'sentiment-lewagon'
BQ_DATASET_ID = 'sentiment_db'

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

#HELPER FUNCTIONS
def download_df_from_bq(table_name, custom_query = ""):
    """
        table_name not used if custom query provided
    """
    #Set up the BigQuery client
    # client = bigquery.Client()

    BQ_TABLE_ID = table_name
    table_ref = f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}"
    if custom_query:
        query = custom_query
    else:
        query = f"SELECT * FROM `{table_ref}`"

    try:
        df = client.query(query).to_dataframe()
        return df
    except Exception as e:
        print(e)

    return None

def upload_df_to_bq(df, table_name):

    try:
        BQ_TABLE_ID = table_name
        table_ref = f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}"

        client = bigquery.Client()

        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND", #append is safer than truncate
        )

        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()

        print(f"✅ Uploaded {job.output_rows} rows to {table_ref}")

    except Exception as e:
        print(f"❌ Failed to upload DataFrame to BigQuery: {e}")



# # Load raw text from bucket
# def get_text_from_bucket(bucket_filepath):
#     bucket_name = "sentiment_chloe-curtis"

#     #load text from bucket
#     try:
#         # Initialize the Google Cloud Storage client
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(bucket_name)

#         # Get a reference to the blob (file)
#         blob = bucket.blob(bucket_filepath)

#         # Download the content of the blob as a string
#         file_content = blob.download_as_text(encoding='utf-8')

#         print(f"Successfully pulled text file '{bucket_filepath}' from bucket '{bucket_name}'.")
#         return file_content

#     except NotFound:
#         print(f"Error: File '{bucket_filepath}' not found in bucket '{bucket_name}'.")
#         return None
#     except Exception as e:
#         print(f"An error occurred while pulling the file: {e}")
#         return None

# #cik helper
# def extract_cik_from_filename(filename):
#     match = re.search(r"_edgar_data_(\d+)_", filename)
#     if match:
#         return match.group(1)
#     else:
#         print(f":warning: No CIK found in: {filename}")
#         return None

# #cik desired
# def is_cik_desired(cik):
#     DESIRED_CIKS = [
#     1090872,    6201, 1158449,  320193, 1551152,    1800, 1467373,
#         796343,    6281,    7084,    8670,  769397, 1002910,    4904,
#         874761,    4977,    5272,  922864, 1267238,  354190, 1086222,
#         915913, 1097149,  766421,  899051, 1579241,    6951,    2488,
#        1037868, 1004434,  318154,  820027, 1053507, 1018724, 1596532,
#        1013462,  315293,   91142, 1841666,    2969,  820313, 1521332,
#        1035443,  731802,  915912, 1730168,    8818, 1410636,    4962,
#         866787,   12927,   70858,   10456,  764478,   10795,   38777,
#          14693, 1685040,  875045, 1390777, 1075531, 2012383,   14272,
#        1383312, 1067983,  885725,  908255, 1037540,  831001,   23217,
#         721371,   18230,  896159, 1374310, 1138118, 1051470,  815097,
#         813672, 1306830, 1324404,  759944,  313927, 1043277, 1091667,
#        1739940,   20286,   21665,   21076,   28412, 1166691, 1156375,
#        1058090,   26172,  811156, 1071739, 1130310,  927628,  711404,
#        1163165,  909832, 1024305,   16732, 1530721,  900075, 1108524,
#         858877,  277948,  723254, 1058290,   64803,   93410,  715957,
#          27904,  315189, 1393612,   29534, 1022079,  882184,  313616,
#        1744489, 1297996,  935703,   29905,  940944,  936340, 1326160,
#         927066, 1090012, 1688568,  712515, 1065088,   31462, 1047862,
#          33185,  827052, 1001250,  915389,   32604,  821189, 1101239,
#         906107,   72741,  920522, 1551182,   65984, 1711269, 1099800,
#        1109357,  746515, 1324424, 1289490,   37996, 1539838,  815556,
#         831259, 1048911, 1031296, 1048695, 1136893,   35527,  850209,
#        1124198,   30625,   37785, 1754301,   34903, 1681459, 1262039,
#        1659166,   40533,   40545,  882095,   40704,   24741, 1467858,
#        1652044,   40987, 1123360, 1121788,  886982,  277135,   45012,
#          46080,   49196, 1359841,  860730,  354950,    4447,  874766,
#        1501585, 1585689,  793952,  859737,  773840,   46765, 1645590,
#          47217,   12659,   48465, 1000228, 1070750,   47111,   49071,
#          51143, 1571949,  874716,   51253, 1110803,  879169,   50863,
#         896878,   51434,   51644, 1111928, 1478242, 1699150, 1020569,
#        1035267,  749251,   49826,  914208,  728535,  833444,   96223,
#         779152,  200406, 1043604,   19617,   72333,   55067,   91576,
#        1601046, 1637459,  879101,  319201,   55785, 1506307, 1170010,
#          21344,   56873,  885639,   60086, 1995807,   58492,  920760,
#         920148, 1707925, 1065696,   59478,  936468,   59558,  352541,
#          60667,  707549,   92380, 1679273, 1489393,  794367, 1141391,
#         912595,  912242, 1048286,   62996,   63276,   63908,  827054,
#         927653, 1059556, 1103982, 1613103, 1099219,  789570,  851968,
#          63754,  916076,   62709,   66740,  865752,  764180, 1285785,
#        1510295,  310158,  895421, 1408198,  789019,   68505,   36270,
#        1037646,  723125, 1513761, 1120193,  753308, 1164727, 1065280,
#        1111711,  320187,  906709, 1133421, 1021860, 1013871,  702165,
#        1002047,   73124,   73309, 1045810,  814453, 1564708,  726728,
#        1039684,   29989, 1341439,  898173,  797468,  723531,   75362,
#         788784,   77476,   78003, 1126328,   80424,   80661,   76334,
#         822416,   75677, 1045609, 1413329,  713676,   77360,  764622,
#          79879,  922224, 1585364, 1137774, 1393311, 1534701,   78239,
#        1050915, 1633917,  804328, 1604778,  884887,  910606,  872589,
#        1281761,  315213,  720005, 1037038,  943819, 1024478,   84839,
#         882835,  745732, 1060391, 1034054,  829224,  316709, 1012100,
#          89800,   91419,   87347, 1040971,   91440,  883241,   92122,
#        1063761,   64040, 1032208, 1881551,   93751, 1137789,   16918,
#          93556,    4127, 1601712,  310764,   96021,  732717,   24545,
#        1260221, 1385157,   96943,   27419,  109198,   97745, 1116132,
#        1526520, 1113169,   86312,  916365,  100493,  946581,   97476,
#         217346, 1336917,  100517,   74208,  352915, 1403568,  731766,
#           5513,  100885, 1090727, 1067701,   36104, 1403161,  103379,
#        1035002, 1396009,  899689, 1442145, 1014473,  875320,  740260,
#         732712,  943452, 1000697, 1618921,  106040,  783325,  766704,
#          72971,  106640,  823768,  107263,  104169, 1365135,  106535,
#        1174922,   72903,   34088,  818479, 1770450, 1524472, 1041061,
#        1136869,  109380, 1555280, 1748790, 1755672, 1666700, 1751788,
#         202058, 1402057,  320335,  832101, 1336920, 1278021,  906163,
#        1283699, 1701605,   52988, 1300514, 1335258, 1373715,  878927,
#        1757898,   92230,   11544,  877212, 1590955, 1466258,   12208,
#        1783180, 1286681, 1093557,    4281, 1781335,  101829, 1094285,
#         860731,  105770, 1370637,   18926,   97210,  945841, 1318605,
#        1786842, 1792044, 1590895, 1463101, 1474735, 1280452, 1413447,
#         921738,  864749, 1100682, 1821825,  857005,  701985,   79282,
#        1682852,  891103,  842023,  858470, 1352010, 1013237, 1419612,
#        1868275, 1179929,   72331,  813828, 1140536,    9389,  906345,
#        1156039, 1418135, 1326801, 1097864, 1705696, 1437107, 1057352,
#        1687229,  947484,   33213, 1274494,  849399, 1004980, 1022671,
#        1389170, 1996862,  814547, 1932393, 1145197, 1069183, 1095073,
#         798354, 1327567,   31791, 1559720, 1393818, 1140859, 1944048,
#        1316835, 1175454, 1725057,  910521,  765880,   48898,  898293,
#        1397187, 1375365, 1543151, 1967680, 1535527, 1609711, 1996810,
#        1404912, 1964738, 1692819, 2011286, 1571996,  922621, 1321655,
#        2005951, 1858681, 1069202, 1811074, 1327811,  815094, 1101215,
#        1578845,  899866,  773910, 1790982,  718877,  816284,  804753,
#         877890, 1358071, 1001082,  783280, 1015780, 1519751,  354908,
#        1132979,   39911,   48039,   40891, 1598014,   54480,   53669,
#         101778,  743316, 1623613,   72207, 1492633, 1378946, 1038357,
#        1087423, 1047122,  719739,   98246,  721689, 1418091,  203527,
#        1339947, 1279363, 1732845, 1168054,  743988, 1424929, 1730175,
#        1596783, 1288784
#     ]
#     return True if cik in DESIRED_CIKS else False

# def get_mda_from_bucket_filepath(bucket_filepath):
#     #item 2 - 10 Q
#     #item 7 - 10 K

#     #pull text from bucket
#     text = get_text_from_bucket(bucket_filepath)

#     if "10-K" in bucket_filepath:
#         filing_type = "10-K"
#     else:
#         filing_type = "10-Q"

#     #extract mda
#     mda = get_mda_from_text(text, filing_type)

#     if not mda:
#         print("did not get any mda for:", bucket_filepath)

#     #return mda
#     return mda
