#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup


def get_article_title(url):
    ret_url = url
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, 'html.parser')
    if 'm.media' in url:
        article = soup.select('div.item_mainnews a.link_cont')
        ret_url = article[0]['href']
        rq = requests.get(ret_url)
        soup = BeautifulSoup(rq.text, 'html.parser')

    return (soup.find('h3', class_='tit_view').text, ret_url)


def is_valid_url(url):
    # 기상특보의 이상한 url인지 아닌지 판별
    return 'http' in url and '기상특보' not in url


if __name__ == '__main__':
    rq = requests.get('https://m.daum.net')
    soup = BeautifulSoup(rq.text, 'html.parser')
  
    articles = []
    main_news_box = soup.select('div.out_ibox div.box_rubics')[0]
    articles += main_news_box.select('ul.list_txt a')
    num_articles = 5 if len(articles) >= 5 else len(articles)

    titles = [get_article_title(article['href']) for article in articles[:num_articles] if is_valid_url(article['href'])]
    
    for title in titles:
        print(title[0])
        print(title[1])