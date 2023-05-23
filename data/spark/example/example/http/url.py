import requests

def detect_url(url):
    resp = requests.get(url)
    return resp.status_code
