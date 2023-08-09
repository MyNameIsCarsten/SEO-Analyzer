import httplib2
from bs4 import BeautifulSoup
import requests

def seo_scraper(URL:str):
    page = requests.get(URL)

    http = httplib2.Http()
    status, response = http.request(URL)

    soup = BeautifulSoup(response, "html.parser")

    status_code = status['status']
    title_text = soup.title.text
    title_len = len(title_text)
    meta_text = soup.find("meta", {"name" : "Description"})["content"]
    meta_len = len(meta_text)
    h1_text = soup.h1.text
    h1_len = len(h1_text)

    return status_code, title_text, title_len, meta_text, meta_len, h1_text, h1_len
