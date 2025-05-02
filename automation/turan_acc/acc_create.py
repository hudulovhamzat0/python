import requests
from bs4 import BeautifulSoup

get_url = "https://turantedris.az/"
post_url = "https://turantedris.az/student/register"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": get_url
}

session = requests.Session()
session.headers.update(headers)

response = session.get(get_url)
if response.status_code != 200:
    print("Ana sayfa erişim hatası:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")
token_input = soup.find("input", {"name": "_token"})
if not token_input:
    print("CSRF token bulunamadı.")
    exit()

csrf_token = token_input.get("value")

form_data = {
    "_token": csrf_token,
    "name": "blackhudul",
    "sinif": "11",
    "gender": "Male",
    "birthday": "2008-08-08",
    "address": "italy",
    "phone": "242",
    "email": "hudul@242.com",
    "password": "ati242"
}

files = {
    "photo": ("", b"", "application/octet-stream")
}

post_response = session.post(post_url, data=form_data, files=files)
print("Durum Kodu:", post_response.status_code)
print("Yanıt:", post_response.text[:500])
