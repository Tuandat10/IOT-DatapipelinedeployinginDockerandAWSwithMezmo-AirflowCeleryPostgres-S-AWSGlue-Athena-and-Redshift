import json
import requests
from utils.constants import HEADERS, API_URL, OUTPUT_FILE
# from webhook.error_information import QUERY_PARAMS
def fetch_logs(QUERY_PARAMS):
    """Fetch logs from Mezmo API."""
    response = requests.get(API_URL, headers=HEADERS, params=QUERY_PARAMS)
    try:
        return response.json().get("lines", [])  # Ensure we handle missing "lines" key
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON response.")
        return []