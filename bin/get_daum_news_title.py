#!/usr/bin/python3

import sys
import requests
from bs4 import BeautifulSoup

def get_article_title(url):
    ret_url = url
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, 'html.parser')
    
    return soup.find('h3', class_='tit_view').text

if __name__ == '__main__':
    print(get_article_title(sys.argv[1]))

