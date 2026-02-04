import os
from dotenv import load_dotenv

load_dotenv()

OKAPI_BASE_URL = os.getenv("OKAPI_BASE_URL", "").rstrip("/")
OKAPI_TENANT = os.getenv("OKAPI_TENANT", "fs00001041")
OKAPI_USERNAME = os.getenv("OKAPI_USERNAME", "")
OKAPI_PASSWORD = os.getenv("OKAPI_PASSWORD", "")
