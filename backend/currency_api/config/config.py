import os

import pytz
from dotenv import load_dotenv

from backend.currency_api.validator import validate_proxy

env = os.environ.get
load_dotenv('./.env')

ALLOWED_ORIGINS = env('ALLOWED_ORIGINS').split(',')
LOG_FILE_PATH = env('LOG_FILE_PATH')

PROXY = env('PROXY') if validate_proxy(env('PROXY')) else None
HEADERS = {
    "user_agents": [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538 "
        "(KHTML, like Gecko) Chrome/36 Safari/538",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36"
    ]
}

MOSCOW_TZ = pytz.timezone('Europe/Moscow')
