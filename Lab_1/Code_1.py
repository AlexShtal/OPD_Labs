from bs4 import BeautifulSoup
import requests

url = "https://hh.ru/?hhtmFrom=vacancy_search_list"
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
page = requests.get(url, headers=headers)

print(page.status_code)

filteredNews = []
allNews = []

soup = BeautifulSoup(page.text)
