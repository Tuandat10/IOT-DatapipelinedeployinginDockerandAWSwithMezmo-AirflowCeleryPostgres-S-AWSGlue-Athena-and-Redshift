#SIMULATE, WAIT FOR REAL INFORMATION
def set_information(unix_start,unix_end,host,levels):
    QUERY_PARAMS = {
        "from": f"{unix_start}",
        "to": f"{unix_end}",
        "levels": f"{levels}",
        "tags": "sasha",
        "hosts": f"{host}"
    }
    return QUERY_PARAMS
# unix_start = 1738368000
# unix_end = 1742688000
# host = input("Enter the mac_id: ")
# QUERY_PARAMS = {
#     "from": f"{unix_start}",
#     "to": f"{unix_end}",
#     "levels": "error,logs",
#     "tags": "sasha",
#     "hosts": f"{host}"
# }