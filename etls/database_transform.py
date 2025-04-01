import json
import pymysql
import requests
import pandas as pd
import time
import pytz
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.types import String
from utils.constants import HOST, PORT, USER,PASSWORD, DATABASE, TABLE_ERROR, TABLE_LOG, BUCKET_NAME
from webhook.after_transforming_error_information import set_information
from etls.get_levelerrorlog_logs import fetch_logs
from etls.process_logs import process_logs,transform_after_logs,process_logs_ver2
from etls.aws_etl import connect_to_s3 
import pymysql
import datetime as dt
import s3fs

# def get_sqlalchemy_engine():
#     return create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
# def get_raw_connection():
#     connection = pymysql.connect(
#         host=HOST,
#         user=USER,
#         password=PASSWORD,
#         database=DATABASE,
#         port=int(PORT),
#     )
#     cursor = connection.cursor()
#     return connection, cursor

def check_and_filter_existence(logs):
    # connection, cursor = get_raw_connection()

    # cursor.execute(f"USE {DATABASE}")
    # cursor.execute(f"SELECT host, timestamp, error_type FROM {TABLE_LOG} WHERE error_event IS NULL")
    # existing_logs = cursor.fetchall()

    # cursor.close()
    # connection.close()
    s3 = connect_to_s3()
    prefix = "raw/"
    file_paths = s3.glob(f"{BUCKET_NAME}/{prefix}*.csv")
    # try:
    df_existing_logs = pd.concat([pd.read_csv(f's3://{file_path}') for file_path in file_paths], ignore_index=True)
    df_existing_logs = df_existing_logs[['host', 'timestamp', 'error_type']]
    # except:
    #     df_existing_logs= None
    # df_existing_logs = pd.DataFrame(existing_logs, columns=["host", "timestamp",'error_type'])
    df_fetched_logs = pd.DataFrame(logs)
    df_existing_logs["timestamp"] = df_existing_logs["timestamp"].astype(str)
    df_fetched_logs["timestamp"] = df_fetched_logs["timestamp"].astype(str)

    df_checked_logs = df_fetched_logs.merge(
        df_existing_logs, on=["host", "timestamp",'error_type'], how="left", indicator=True
    )

    checked_logs = df_checked_logs[df_checked_logs["_merge"] == "left_only"].drop(columns=["_merge", "file"])
    checked_logs['timestamp'] = pd.to_datetime(checked_logs['timestamp']) + pd.Timedelta(days=1)
    checked_logs = checked_logs[['host', 'message', 'timestamp', 'level', 'error_type']]
    return checked_logs
def load_data_to_csv(data,path):
    data.to_csv(path,index=False)

# def save_logs_to_error_table(logs):
#     """Save logs to the database."""
#     logs = logs.convert_dtypes().astype(str)
#     engine = get_sqlalchemy_engine()
#     logs.to_sql(
#         name=TABLE_LOG,
#         con=engine,
#         if_exists="append",
#         index=False,
#     )

#     print("✅ Logs successfully saved.")
def windows_function(df):
    """Apply window functions to DataFrame."""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by=['host','timestamp'])
    df['prev_timestamp'] = df.groupby('host')['timestamp'].shift(1)
    df['time_diff']= df['timestamp'] - df['prev_timestamp']
    df_windows = df[(df['time_diff'].isna()) | (df['time_diff'] > pd.Timedelta(days=1))].drop(columns=['prev_timestamp','time_diff'])
    return df_windows
def save_to_log_table(logs):
    """Save logs to the database."""
    for _, row in logs.iterrows():
        host = row["host"]
        ts = pd.to_datetime(row["timestamp"])
        ts = ts + dt.timedelta(hours=13) - dt.timedelta(days=1)
        unix_end = int(ts.timestamp() * 1000) + 60000
        unix_start = unix_end - 86400000
        levels = 'error,log,debug'
        query_params = set_information(unix_start,unix_end,host,levels)
        try:
            craw_logs = fetch_logs(query_params)
            extracted_logs = process_logs_ver2(craw_logs)
            df = transform_after_logs(extracted_logs)
            df['error_event'] = row['message']
            df['error_type'] = row['error_type']
            df['timestamp'] = row['timestamp']
            # engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
            # df.to_sql(name=TABLE_LOG, con=engine, if_exists="append", index=False)
            return df
        except:
            pass