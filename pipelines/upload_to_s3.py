import os
import sys
from etls.aws_etl import connect_to_s3, create_bucket_if_not_exists,upload_to_s3_syntax
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.constants import BUCKET_NAME

# def etl_final_log(**kwargs):
#     ti = kwargs['ti']
#     checked_logs = ti.xcom_pull(task_ids='process_logs',key="return_value")
#     if checked_logs is None or checked_logs.empty:
#         print("No logs found.")
#         return None
#     df_windows= windows_function(checked_logs)
#     save_to_log_table(df_windows)

def upload_to_s3(**kwargs):
    ti = kwargs['ti']
    file_path, file_path_raw = ti.xcom_pull(task_ids='process_logs',key="return_value")
    prefix_filepath = 'raw_full_log'
    prefix_filepath_raw = 'raw'
    if file_path is None:
        print("No logs found.")
        return None
    # Upload the DataFrame to S3
    s3 = connect_to_s3()
    create_bucket_if_not_exists(s3, BUCKET_NAME)
    upload_to_s3_syntax(s3,file_path,prefix_filepath,BUCKET_NAME,file_path.split('/')[-1])
    upload_to_s3_syntax(s3,file_path_raw,prefix_filepath_raw,BUCKET_NAME,file_path_raw.split('/')[-1])
    pass