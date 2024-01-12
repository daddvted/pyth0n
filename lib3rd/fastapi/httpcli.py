
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

s = requests.Session()

retries = Retry(total=5,
                status_forcelist=[429, 500, 502, 503, 504])

s.mount('http://', HTTPAdapter(max_retries=retries))

s.get('http://192.168.6.78:10086/sleep')
