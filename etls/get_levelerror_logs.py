import json
import requests
from utils.constants import HEADERS, API_URL, OUTPUT_FILE

def fetch_logs(query):
    """Fetch logs from Mezmo API."""
    response = requests.get(API_URL, headers=HEADERS, params=query)
    try:
        return response.json().get("lines", [])  # Ensure we handle missing "lines" key
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON response.")
        return []
