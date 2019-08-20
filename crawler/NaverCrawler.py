#!/usr/bin/python3
import os
import argparse
import sys
import datetime
import time
import json
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_dir', type=str, help='The directory where crawled news articles are going to be saved.')
    parser.add_argument('date', type = str, help='A date to crawl.')
    args = parser.parse_args()

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)

    return args


class NaverCrawler:
    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        self.base_url = u'https://news.naver.com/main/ranking/popularMemo.nhn?rankingType=popular_memo&'

    def __del__(self):
        self.browser.quit()

    def get_targets(self, date):
        # get politics 100, economy 101, social 102, life 103, global 104, IT news 105, photo 003, TV 115 news's urls
        url_dic = dict()
        sections = []
        [sections.append(str(i)) for i in range(100, 106, 1)]
        sections.append('003')
        sections.append('115')

        for s in sections:
            query = "sectionId=%s&date=%s" % (s, date)
            url = self.base_url + query
            self.browser.get(url)
            a_list = self.browser.find_elements_by_xpath("//a[contains(@class, 'count_cmt')]")
            urls = []
            for a in a_list:
                urls.append(a.get_attribute('href'))
            url_dic[s] = urls

        return url_dic

    def parse_news(self, url):
        try:
            WebDriverWait(self.browser, 3).until(
                expected_conditions.presence_of_element_located((By.ID, 'articleTitle'))
            )
        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException):
            return
        a_id = re.search(r'.*?&aid=(\d+)', url).group(1)
        news_title = self.browser.find_element_by_xpath("//h3[contains(@id, 'articleTitle')]//a").text
        news_time = []
        for time_info in self.browser.find_elements_by_class_name('t11'):
            news_time.append(time_info.text)
        if len(news_time) < 2:
            news_time.append(news_time[0])
        news_press = self.browser.find_element_by_xpath("//div[contains(@class, 'press_logo')]//img").get_attribute('title')
        news = {'type' : 'news', 'id' : a_id, 'title' : news_title, 'time' : news_time[0], 'modi_time' : news_time[1], 'press' : news_press}
        return news

    def scroll_to_end(self):
        try:
            WebDriverWait(self.browser, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'u_cbox_txt_usercomment'))
            )
            more_box = self.browser.find_element_by_xpath("//a[contains(@class, 'u_cbox_btn_more')]")
            box_loc = more_box.location
            while True:
                #self.browser.execute_script("arguments[0].scrollIntoView();", more_box)
                more_box.click()
                time.sleep(0.2)
                more_box = self.browser.find_element_by_xpath("//a[contains(@class, 'u_cbox_btn_more')]")
                

                new_loc = more_box.location
                if box_loc == new_loc: return
                box_loc = new_loc

        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException):
            return           

    def open_reply(self, comment):
        try:
            reply_btn = comment.find_element_by_css_selector('a.u_cbox_btn_reply')
            reply_btn.click()
        except NoSuchElementException:
            return
        try:
            more_reply_box = comment.find_element_by_css_selector('span.u_cbox_page_more')
            box_loc = more_reply_box.location

            while True:
                more_reply_box.click()
                time.sleep(0.2)
                more_reply_box = comment.find_elemet_by_css_selector('span.u_cbox_page_more')
                new_loc = more_reply_box.location
                if box_loc == new_loc:
                    return
                box_loc = new_loc
        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException):
            return

    def parse_comment(self, comment, is_reply=False):
        data = {}
        try:
            data['text'] = comment.find_element_by_css_selector('span.u_cbox_contents').text
        except NoSuchElementException:
            return None

        c_data = comment.get_attribute('class')
        c_data = c_data.split(' ')[1]
        
        c_id = comment.get_attribute('data-info')
        data['id'] = (c_id.split(',')[0]).split(':')[1]
        
        data['time'] = comment.find_element_by_css_selector('span.u_cbox_date').text

        data['like'] = int(comment.find_element_by_css_selector('em.u_cbox_cnt_recomm').text)
        data['dislike'] = int(comment.find_element_by_css_selector('em.u_cbox_cnt_unrecomm').text)

        if not is_reply and int(comment.find_element_by_css_selector('span.u_cbox_reply_cnt').text) > 0:
            self.open_reply(comment)
            data['reply'] = {}
            comment = self.browser.find_element_by_css_selector('li.%s' % (c_data))
            reply_list = comment.find_elements_by_css_selector('div.u_cbox_reply_area li')
            for reply in reply_list:
                r_data = self.parse_comment(reply, is_reply=True)
                if r_data:
                    data['reply'][r_data['id']] = r_data

        return data

    def crawl_url(self, url):
            self.browser.get(url)
            news = self.parse_news(url)
            
            news['comment'] = {}
            self.scroll_to_end()
            cmt_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'u_cbox_list')]//li")
            for _, cmt in enumerate(cmt_list):
                data = self.parse_comment(cmt)
                if data:
                    news['comment'][data['id']] = data
            return news

    
    def crawl(self, date, save_path):
        dir_path = os.path.join(save_path, date)
        os.makedirs(dir_path, exist_ok=True)

        url_dic = self.get_targets(date)
        sections = []
        # get politics 100, economy 101, social 102, life 103, global 104, IT news 105, photo 003, TV 115
        sections.append(('100', 30, 'politics'))
        sections.append(('101', 10, 'economy'))
        sections.append(('102', 20, 'social'))
        sections.append(('103', 6, 'life'))
        sections.append(('104', 10, 'global'))
        sections.append(('105', 3, 'IT'))
        sections.append(('003', 31, 'photo'))
        sections.append(('115', 15, 'TV'))
        
        for s in sections:
            for i in range(s[1]):
                print("crawling %s news %d/%d" % (s[2], i + 1, s[1]), file=sys.stderr)
                news_data = self.crawl_url(url_dic[s[0]][i])
                with open(os.path.join(dir_path, news_data['id']), 'w', encoding='utf8') as f:
                    json.dump(news_data, f, ensure_ascii=False)
                    



if __name__ == '__main__':
    os.environ['MOZ_HEADLESS'] = '1'
    args = get_arguments()
    crawler = NaverCrawler()
    print('start crawling', file=sys.stderr)
    crawler.crawl(args.date, args.out_dir)
    
