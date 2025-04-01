import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from etls.process_logs import process_logs
from etls.database_transform import check_and_filter_existence, load_data_to_csv,windows_function, save_to_log_table
from utils.constants import OUTPUT_FILE
def process_and_check_existence(**kwargs):
    ti = kwargs['ti']
    logs = ti.xcom_pull(task_ids="fetch_mezmo_logs",key="return_value")
    if not logs:
        print("No logs found.")
        return None
    extracted_logs = process_logs(logs)
    checked_logs= check_and_filter_existence(extracted_logs)
    df_windows = windows_function(checked_logs)
    final_output = save_to_log_table(df_windows)
    filename = kwargs['params']['file_name']
    file_name_raw = kwargs['params']['file_name'] + '_raw'
    file_path_raw = f'{OUTPUT_FILE}/{file_name_raw}.csv'
    file_path = f'{OUTPUT_FILE}/{filename}.csv'
    load_data_to_csv(checked_logs, file_path_raw)
    load_data_to_csv(final_output, file_path)
    return file_path,file_path_raw