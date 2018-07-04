#!/usr/bin/python3
import os
import time
import datetime
import json
import argparse
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DaumCrawler:
    def __init__(self):
        os.environ['MOZ_HEADLESS'] = '1'
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(0)
        self.base_url = u'http://media.daum.net/ranking/bestreply/?regDate='
        self.wait = WebDriverWait(self.browser, 1.5)

    def crawl(self, date=None, url=None):
        try:
            if date:
                urls = self.get_targets(date)
                print("start crawling", date)
            elif url:
                urls = [url]
            else:
                urls = []
        
            self.browser.quit()
            for url in urls:
                try:
                    self.browser = webdriver.Firefox()
                    self.browser.get(url)

                    # remove vod bar
                    self.browser.execute_script("""
                    var e = document.querySelector(".vod_open");
                    if (e)
                        e.parentNode.removeChild(e);
                    """)

                    print('crawling', url)

                    news = self.parse_news(url)
                    print('news article parsed')
                    news['comment'] = {}

                    print('start scroll to end of page')
                    self.scroll_to_end()
                    print('\nscrolled to end of page')
                    print('start crawling news comment')
                    cmt_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_comment')]//li")
                    cmt_num = len(cmt_list)
                    for i, cmt in enumerate(cmt_list):
                        data = self.parse_comment(cmt)
                        if data:
                            news['comment'][data['id']] = data
                        print('\rcomment %d/%d is done' % (i+1, cmt_num), end='')
                    print('')

                    #write
                    json_data = json.dumps(news, ensure_ascii=False)
                    save_path = 'crawled_data/daum_news/' + str(date)
                    os.makedirs(save_path, exist_ok=True)
                    f = open(save_path + '/' + news['id'], 'w', encoding='utf-8')
                    f.write(json_data)
                    print(url, 'is crawled')
                except Exception as e:
                    with open("error.log", 'a') as err_file:
                        log_text = str(date) + ", " + str(url) + ", " + str(e) + "\n"
                        err_file.write(log_text)
                finally:
                    self.browser.quit()
                    self.browser = webdriver.Firefox()

        except Exception as e:
            with open("error.log", 'a') as err_file:
                log_text = str(date) + ", " + str(url) + ", " + str(e) + "\n"
                err_file.write(log_text)
            self.browser.quit()
            self.browser = webdriver.Firefox()


    def parse_news(self, url):
        news_id = url.split('/')[-1]
        news_title = self.browser.find_element_by_xpath("//h3[contains(@class, 'tit_view')]").text
        news_open_time = None
        news_modi_time = None
        news_reporter = None
        for txt_info in self.browser.find_elements_by_xpath("//span[contains(@class, 'info_view')]//span[contains(@class, 'txt_info')]"):
            info = txt_info.text
            if info[0] == '입' and info[1] == '력': news_open_time = info[2:]
            elif info[0] == '수' and info[1] == '정': news_modi_time = info[2:]
            else : news_reporter = info
        news_press = self.browser.find_element_by_xpath("//div[contains(@class, 'head_view')]//img").get_attribute('alt')
        news_body = self.browser.find_element_by_xpath("//div[contains(@class, 'article_view')]").text
        news = {'type' : 'news', 'id' : news_id, 'title' : news_title, 'time' : news_open_time, 'modi_time' : news_modi_time, 'press' : news_press, 'reporter' : news_reporter, 'text' : news_body }
        return news

    def scroll_to_end(self):
        try:
            i = 0
            more_box = self.browser.find_element_by_css_selector("div.cmt_box>div.alex_more a")
            box_loc = more_box.location
            while True:
                i += 1
                more_box.click()
                print('\r' + str(i) + ' click()', end='')
                start_time = time.time()
                while len(more_box.find_elements_by_tag_name('span')) < 2:
                    if time.time()-start_time >= 10:
                        return
                    time.sleep(0.2)
                    more_box = self.browser.find_element_by_css_selector("div.cmt_box>div.alex_more a")
                new_loc = more_box.location
                if box_loc == new_loc:
                    return
                box_loc = new_loc
        except (NoSuchElementException, StaleElementReferenceException):
            return

    def open_reply(self, comment):
        try:
            reply_btn = comment.find_element_by_css_selector("div.box_reply button.reply_count span.num_txt")
            reply_btn.click()
        except NoSuchElementException:
            return False

        try:
            more_reply_box = comment.find_element_by_css_selector("div.reply_wrap>div.alex_more a")
            box_loc = more_reply_box.location
            while True:
                more_reply_box.click()
                start_time = time.time()
                while len(more_reply_box.find_elements_by_tag_name('span')) < 2:
                    if time.time()-start_time >= 10:
                        return True
                    time.sleep(0.2)
                    more_reply_box = comment.find_element_by_css_selector("div.reply_wrap>div.alex_more a")
                new_loc = more_reply_box.location
                if box_loc == new_loc:
                    return True
                box_loc = new_loc
        except (NoSuchElementException, StaleElementReferenceException):
            return True

    def get_targets(self, date):
        query = str(date)
        url = self.base_url + query
#url = "http://media.daum.net/ranking/kkomkkom/"
        self.browser.get(url)

        li_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_news2')]//li")
        
        urls = []
        for li in li_list:
            tag_a = li.find_element_by_tag_name('a')
            urls.append(tag_a.get_attribute("href"))
        return urls

    def parse_comment(self, comment, is_reply=False):
        data = {}

        try:
            data['text'] = comment.find_element_by_css_selector('p.desc_txt').text
        except NoSuchElementException:
            return None

        if not is_reply:
            data['id'] = int(comment.get_attribute('id').replace('comment',''))
        else:
            data['id'] = int(comment.get_attribute('data-reactid').split('.')[-1][1:])
        data['name'] = comment.find_element_by_css_selector('a.link_nick').text

        cmt_time_txt = comment.find_element_by_css_selector('span.txt_date').text
        if len(cmt_time_txt) > 0:
            if '분' in cmt_time_txt:
                now = datetime.datetime.now()
                now = now - datetime.timedelta(minutes=int(cmt_time_txt.replace('분전', '')))
                cmt_time = time.mktime(now.timetuple())
            elif '시간' in cmt_time_txt:
                now = datetime.datetime.now()
                now = now - datetime.timedelta(hours=int(cmt_time_txt.replace('시간전','')))
                cmt_time = time.mktime(now.timetuple())
            elif '조금' in cmt_time_txt:
                now = datetime.datetime.now()
                cmt_time = time.mktime(now.timetuple())
            else:
                cmt_time_txt.replace(' ','')
                dt = datetime.datetime.strptime(cmt_time_txt, '%Y.%m.%d.%H:%M')
                cmt_time = time.mktime(dt.timetuple())
            data['time'] = cmt_time

        if not is_reply:
            data['like'] = int(comment.find_element_by_css_selector('button.btn_recomm span.num_txt').text)
            data['dislike'] = int(comment.find_element_by_css_selector('button.btn_oppose span.num_txt').text)

            if self.open_reply(comment):
                data['reply'] = {}
                reply_list = comment.find_elements_by_css_selector('ul.list_reply li')
                for reply in reply_list:
                    r_data = self.parse_comment(reply, is_reply=True)
                    if r_data:
                        data['reply'][r_data['id']] = r_data

        return data

def get_date_to_crawl():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--date', nargs='+', help='date to crawl. the format is YYYYMMDD. ex)20180211')
    group.add_argument('-u', '--url', help='make \'date\' parameter to get a url')
    group.add_argument('--duration', nargs=2, help='crawling news between two dates')
    args = parser.parse_args()
    if args.url:
        return ('url', args.url)
    elif args.duration:
        d_first = datetime.datetime.strptime(args.duration[0], "%Y%m%d").date()
        d_last = datetime.datetime.strptime(args.duration[1], "%Y%m%d").date()
        dates = []
        while d_first <= d_last:
            dates.append(d_first.strftime("%Y%m%d"))
            d_first += datetime.timedelta(days=1)
        return ('date', dates)
    else:
        return ('date', [d for d in args.date])

if __name__ == '__main__':
    dt = get_date_to_crawl()
    dc = DaumCrawler()
    if dt[0] == 'url':
        dc.crawl(url=dt[1])
    elif dt[0] == 'date':
        print("articles on following dates is going to be crawled: ")
        for d in dt[1]:
            print(d, end=', ')
        print("")
        for d in dt[1]:
            dc.crawl(date=d)
