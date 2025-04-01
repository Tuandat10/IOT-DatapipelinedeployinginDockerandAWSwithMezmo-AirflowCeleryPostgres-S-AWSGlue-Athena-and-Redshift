#SIMULATE, WAIT FOR REAL INFORMATION
def set_query(unix_start, unix_end):
    QUERY_PARAMS = {
        "from": f"{unix_start}",
        "to": f"{unix_end}",
        "levels": "log,error",
        "tags": "sasha",
        "apps": "sasha.agent,sasha.device",
        # "hosts": f"{host}",
        "query":"\"Teams: Sending teams message: 🔴 Scheduled dose missed.\" OR \"Teams: Sending teams message: 🪫 Running on low battery.\" OR \"Teams: Sending teams message: 🔋 Running on battery.\" OR  \"Ending post-administration\" OR \"Teams: Sending teams message: ⏳ Pre-administration\" OR \"OUT OF SYNC\" OR \"Sachet edge not found after loading\""
    }
    return QUERY_PARAMS
