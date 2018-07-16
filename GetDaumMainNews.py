#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup


def get_article_title(url):
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, 'html.parser')
    return soup.find('h3', class_='tit_view').text


if __name__ == '__main__':
    rq = requests.get('http://media.daum.net')
    soup = BeautifulSoup(rq.text, 'html.parser')
  
    articles = []
    articles += soup.select('ul.list_view strong.tit_g a.link_txt')
    articles += soup.select('ul.list_headline strong.tit_g a.link_txt')
   
    titles = [get_article_title(article['href']) for article in articles]
    
    for title in titles:
        print(title)
