from datetime import datetime, timezone, timedelta
import json
import pandas as pd
from datetime import datetime, timezone, timedelta

def process_logs(logs):
    """Process and extract necessary fields from logs, including error type detection."""
    extracted_logs = []
    
    for log in logs:
        log_message = log.get("_line", "No message")
        timestamp_unix = log.get("_ts", 0)
        log_level = log.get("level", "Unknown")
        log_file = log.get("_file", "Unknown")
        log_host = log.get("_host", "Unknown")

        # Convert timestamp to UTC (adjusting -13 hours if needed)
        timestamp_readable = (datetime.fromtimestamp(timestamp_unix / 1000, tz=timezone.utc) - timedelta(hours=13)).strftime('%Y-%m-%d %H:%M:%S UTC')

        # Detect error type based on message content
        message_lower = log_message.lower()
        if "dose missed" in message_lower:
            error_type = "missed dose"
        elif "low battery" in message_lower:
            error_type = "low battery"
        elif "running on battery" in message_lower:
            error_type = "running on battery"
        elif "ending post-administration" in message_lower:
            error_type = "post-admin"
        elif "pre-administration" in message_lower:
            error_type = "pre_admin"
        elif "out of sync" in message_lower or "sachet edge not found after loading" in message_lower:
            error_type = "out of sync"
        else:
            error_type = None  # or "" if preferred

        extracted_logs.append({
            "timestamp": timestamp_readable,
            "message": log_message,
            "level": log_level,
            "file": log_file,
            "host": log_host,
            "error_type": error_type
        })

    return extracted_logs

def process_logs_ver2(logs):
    """Process and extract necessary fields from logs."""
    extracted_logs = []
    for log in logs:
        log_message = log.get("_line", "No message")
        timestamp_unix = log.get("_ts", 0)
        log_level = log.get("level", "Unknown")
        log_file = log.get("_file", "Unknown")
        log_host = log.get("_host", "Unknown")
        
        # Ensure correct UTC conversion
        # IF THE TIMESTAMP IN MEZMO IS NOT CORRECT USE THE CODE COMMENTED BELOW
        timestamp_readable = (datetime.fromtimestamp(timestamp_unix / 1000, tz=timezone.utc) - timedelta(hours=13) + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S UTC')
        # timestamp_readable = (datetime.fromtimestamp(timestamp_unix / 1000, tz=timezone.utc)).strftime('%Y-%m-%d %H:%M:%S UTC')
        # print("a"*80)
        extracted_logs.append({
            "timestamp": timestamp_readable,
            "message": log_message,
            "level": log_level,
            "file": log_file,
            "host": log_host
        })
    return extracted_logs
def aggregate_logs(group):
    """Aggregate logs by host and level with special filtering for DEBUG SCAN event logs."""

    # Filter and transform each row based on the condition
    log_list = group.apply(
        lambda row: {
            "message": row['message'],
            "timestamp": row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            "level": row['level']
        } if row['level'].upper() != 'DEBUG' or ('SCAN event' in row['message']) else None,
        axis=1
    )

    # Remove None entries (i.e., filtered-out DEBUG messages)
    log_list = [log for log in log_list if log is not None]

    # ✅ Sort log_list by timestamp (oldest first)
    log_list.sort(key=lambda x: x['timestamp'])

    # Get the max timestamp where level is ERROR
    error_rows = group[group['level'].str.upper() == 'ERROR']
    if not error_rows.empty:
        max_error_ts = error_rows['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')
    else:
        max_error_ts = None  # or group['timestamp'].max().strftime(...) if you want fallback

    return pd.Series({
        "message": log_list,
        "timestamp": max_error_ts,
        "level": 'log,error,debug'
    })

def transform_after_logs(logs):
    """Transform logs into DataFrame."""
    df = pd.DataFrame(logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_grouped = df.groupby('host').apply(aggregate_logs).reset_index()
    df_grouped['message'] = df_grouped['message'].apply(json.dumps)
    return df_grouped
