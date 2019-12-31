#!/usr/bin/python3
import os
import time
import datetime
import json
import argparse
import sys
import functools
from multiprocessing import Pool, Queue
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCRIPT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))

def get_new_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    #return webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    return webdriver.Chrome(chrome_options=options
                            ,executable_path='/home/cjy/GraduationProject/crawler/chromedriver') 

class DaumCrawler:
    def __init__(self):
        self.browser = get_new_browser()
        self.base_url = u'http://media.daum.net/ranking/bestreply/?regDate='


    def __del__(self):
        self.browser.quit()


    def get_url_from_date(self, date):
        try:
            urls = self.get_targets(date)
            return urls
        except Exception as e:
            err_text =  "ERROR: While getting URLs from " + str(date) + ", " + str(e)
            print(err_text, file=sys.stderr)
            self.browser.quit()
            self.browser = get_new_browser()
            return []

    @staticmethod
    def crawl_url(browser, url):
        try:
            browser.get(url)

            # remove vod bar
            browser.execute_script("""
            var e = document.querySelector(".vod_open");
            if (e)
                e.parentNode.removeChild(e);
            """)

            news = DaumCrawler._parse_news(browser, url)
            news['comment'] = {}

            DaumCrawler._scroll_to_end(browser)
            cmt_list = browser.find_elements_by_css_selector("ul.list_comment > li")
            assert len(cmt_list) > 0, "the comment list has no comment"
            for _, cmt in enumerate(cmt_list):
                data = DaumCrawler._parse_comment(cmt)
                if data:
                    news['comment'][data['id']] = data

            #write
            return news
        except Exception as e:
            err_text = "ERROR: in " + str(url) + ", " + str(e)
            print(err_text, file=sys.stderr)
        finally:
            browser.quit()


    @staticmethod
    def _parse_news(browser, url):
        news_id = url.split('/')[-1]
        news_title = browser.find_element_by_xpath("//h3[contains(@class, 'tit_view')]").text
        news_open_time = None
        news_modi_time = None
        news_reporter = None
        for txt_info in browser.find_elements_by_xpath("//span[contains(@class, 'info_view')]//span[contains(@class, 'txt_info')]"):
            info = txt_info.text
            if info[0] == '입' and info[1] == '력': news_open_time = info[2:]
            elif info[0] == '수' and info[1] == '정': news_modi_time = info[2:]
            else : news_reporter = info
        news_press = browser.find_element_by_xpath("//div[contains(@class, 'head_view')]//img").get_attribute('alt')
        news_body = browser.find_element_by_xpath("//div[contains(@class, 'article_view')]").text
        news = {'type' : 'news', 'id' : news_id, 'title' : news_title, 'time' : news_open_time, 'modi_time' : news_modi_time, 'press' : news_press, 'reporter' : news_reporter, 'text' : news_body }
        return news

    @staticmethod
    def _scroll_to_end(browser):
        more_box = browser.find_element_by_css_selector("div.cmt_box>div.alex_more a")
        box_loc = more_box.location
        while True:
            more_box.click()
            start_time = time.time()
            while len(more_box.find_elements_by_tag_name('span')) < 2:
                if time.time()-start_time >= 10:
                    return
                time.sleep(0.2)
                more_box = browser.find_element_by_css_selector("div.cmt_box>div.alex_more a")
            new_loc = more_box.location
            if box_loc == new_loc:
                return
            box_loc = new_loc

    @staticmethod
    def _open_reply(comment):
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
        self.browser.get(url)

        li_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_news2')]//li")
        
        urls = []
        for li in li_list:
            tag_a = li.find_element_by_tag_name('a')
            urls.append(tag_a.get_attribute("href"))
        return urls

    @staticmethod
    def _parse_comment(comment, is_reply=False):
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
            data['like'] = int(comment.find_elements_by_css_selector('button.btn_recomm span.num_txt')[-1].text)
            data['dislike'] = int(comment.find_elements_by_css_selector('button.btn_oppose span.num_txt')[-1].text)

            # if DaumCrawler._open_reply(comment):
                # data['reply'] = {}
                # reply_list = comment.find_elements_by_css_selector('ul.list_reply li')
                # for reply in reply_list:
                    # r_data = DaumCrawler._parse_comment(reply, is_reply=True)
                    # if r_data:
                        # data['reply'][r_data['id']] = r_data

        return data

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_dir', type=str, help='The directory where crawled news articles are going to be saved.')
    parser.add_argument('-p', '--process_num', type=int, help='number of worker process')
    args = parser.parse_args()

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)

    return args

def get_urls_to_be_crawled(dates, crawler):
    urls = []
    for date in dates:
        urls.append((date, crawler.get_url_from_date(date)))
    print("Following news articles are going to be crawled:", file=sys.stderr)
    for (_, url) in urls:
        print("\n".join(url), file=sys.stderr)

    return urls

def crawl(url, date):
    news_data = DaumCrawler.crawl_url(get_new_browser(), url)
    return (url, news_data, date)

completed_num = 0

def save_result(result, total_num, save_path):
    global completed_num
    completed_num += 1
    url, news_data, date = result
    if news_data is None:
        return
    dir_path = os.path.join(save_path, date)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, news_data["id"]), 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False)
    print("Crawled %s, %d/%d has done" % (url, completed_num, total_num), file=sys.stderr)

if __name__ == '__main__':
    #os.environ['MOZ_HEADLESS'] = '1'
    args = get_arguments()
    
    crawler = DaumCrawler()
    dates = [date.strip() for date in sys.stdin.readlines()]
    urls = get_urls_to_be_crawled(dates, crawler)

    pool = Pool(processes=args.process_num)

    print('start crawling', file=sys.stderr)
    results = []
    total_len = functools.reduce(lambda x,y: x+y, (len(url) for _, url in urls))
    for date, url in urls:
        results += [pool.apply_async(crawl, (u,date), callback=lambda x: save_result(x, total_len, args.out_dir)) for u in url]
    for result in results:
        result.wait()

    for date in dates:
        print(os.path.realpath(os.path.join(args.out_dir, date)))
