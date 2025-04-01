import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipelines.fetch_raw_log_Mezmo_pipeline import fetch_raw_mezmo
from pipelines.process_check_existence_log import process_and_check_existence
from pipelines.ETL_final_log import etl_final_log
def run_pipeline():
    """Run the entire pipeline."""
    logs= fetch_raw_mezmo()
    checked_logs= process_and_check_existence(logs)
    etl_final_log(checked_logs)
if __name__ == "__main__":
    run_pipeline()