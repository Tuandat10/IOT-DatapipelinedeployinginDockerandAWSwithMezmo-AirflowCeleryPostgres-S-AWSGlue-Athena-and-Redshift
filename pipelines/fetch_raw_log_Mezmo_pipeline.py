import os
import json
import requests
from datetime import datetime, timezone, timedelta
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etls.get_levelerror_logs import fetch_logs

from webhook.error_information import set_query
def fetch_raw_mezmo(**kwargs):
    """Main function to execute log retrieval and processing."""
    try:
        unix_start = kwargs['params']['unix_start']
        unix_end = kwargs['params']['unix_end']
        query=  set_query(unix_start, unix_end)
        logs = fetch_logs(query)
        return logs
    except:
        print("The Mac_id does not have any logs")
        return None
