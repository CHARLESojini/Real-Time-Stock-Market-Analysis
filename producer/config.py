import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename='stock_data_logs.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

BASEURL = "alpha-vantage.p.rapidapi.com"

url = f"https://{BASEURL}/query"

headers = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
    "x-rapidapi-host": BASEURL,
    "Content-Type": "application/json"
}
