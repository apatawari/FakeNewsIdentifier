import urllib
import requests
import re
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector


def parse_content(url):
    
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.text, from_encoding=encoding, features="html5lib")
    print(content)
    if type(content) != None:
    	text = content.find('div', attrs={"class": "Normal"}).text
    	return text


# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

query = "Breaking News from CNN :- Dr. Li Wenliang"

query = query.replace(' ', '+')
URL = "https://google.com/search?q="+query

headers = {"user-agent": USER_AGENT}
resp = requests.get(URL, headers=headers)

http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, from_encoding=encoding, features="html5lib")

links = []

for link in soup.find_all('a', href=True, attrs={'href': re.compile("^http://")}):
    if link['href'] != "#":
        links.append(link['href'])
        print(parse_content(link['href']))

