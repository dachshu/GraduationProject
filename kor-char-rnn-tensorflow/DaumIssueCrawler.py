import os
import time
from selenium import webdriver
from random import *


class DaumIssueCrawler:
    #정치 이슈에 대해 검색
    def __init__(self):
        os.environ['MOZ_HEADLESS'] = '1'
        self.browser = webdriver.Firefox()
        self.base_url = u'http://media.daum.net/issue/'

    def crawling(self):
        query = "politics/1"
        url = self.base_url + query
        self.browser.get(url)
        time.sleep(1)

        issue_li_list = self.browser.find_elements_by_xpath("//ul[contains(@id, 'issueList')]//li")
        issues = []
        for li in issue_li_list:
            issues.append(li.find_element_by_class_name('link_txt').text)
        
        return issues

    def get_issue_word(self):
        issues = self.crawling()
        issue_words = []
        for issue in issues:
            words = issue.split(" ")
            if len(words) > 0:
                if words[0][-1] == ',' and len(words) > 1: issue_words.append(words[1])
                else: issue_words.append(words[0])
        i = randint(0, (len(issue_words))/2)
        return issue_words[i]

        


if __name__ == '__main__':
    crawler = DaumIssueCrawler()
    print(crawler.get_issue_word())

