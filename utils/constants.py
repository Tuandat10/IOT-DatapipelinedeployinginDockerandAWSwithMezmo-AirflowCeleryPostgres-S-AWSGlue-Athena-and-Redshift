import configparser
import os
parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))
#API ACCESS
ACCESS_KEY = parser.get("api","access_key")
API_URL = parser.get("api","url")
HEADERS = {"servicekey": ACCESS_KEY}
OUTPUT_FILE = os.path.join(os.getcwd()+"/data/output/", "extracted_logs.json")
#MYSQL CONNECTION
HOST = parser.get("mysql","host")
PORT = parser.get("mysql","port")
USER = parser.get("mysql","username")
PASSWORD = parser.get("mysql","password")
DATABASE = parser.get("mysql","database")
TABLE_ERROR = parser.get("mysql","table_error")
TABLE_LOG = parser.get("mysql","table_log")
#AWS S3 BUCKET 
BUCKET_NAME = parser.get("aws","aws_bucket_name")
AWS_ACCESS_KEY_ID = parser.get("aws","aws_access_key_id")
AWS_SECRET_ACCESS_KEY = parser.get("aws","aws_secret_access_key")
AWS_REGION_NAME = parser.get("aws","aws_region")
# FILE_PATH
INPUT_PATH = parser.get("file_paths","input_path")
OUTPUT_FILE = parser.get("file_paths","output_path")
