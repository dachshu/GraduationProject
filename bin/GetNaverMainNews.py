#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup



if __name__ == '__main__':
    rq = requests.get('https://m.naver.com/')
    soup = BeautifulSoup(rq.text, 'html.parser')
  
    articles = []
    main_news_box = soup.select('ul.uio_text')[0]
    articles += main_news_box.select('li.ut_item a')
    articles += main_news_box.select('li.ut_item2 div.ut_div a.utd_a')
    urls = [article['href'] for article in articles]

    urls = [url for url in urls if url is not None]
    
    for url in urls:
        print(url)
