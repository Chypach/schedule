from os import getenv
from dotenv import load_dotenv
import re


load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")

def is_valid_time(time_str):
    pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
    return bool(re.match(pattern, time_str))