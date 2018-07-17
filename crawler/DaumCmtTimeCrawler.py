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

ARCHIVE_PATH = "time_archive"

class DaumCrawler:
    def __init__(self):
        os.environ['MOZ_HEADLESS'] = '1'
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(0)
        self.base_url = u'http://media.daum.net/ranking/bestreply/?regDate='
        self.wait = WebDriverWait(self.browser, 1.5)

    def crawl(self, date=None, url=None):
        self.date = date
        if date:
            try:
                urls = self.get_targets(date)
                print("start crawling", date)
            except Exception as e:
                with open("error.log", 'a') as err_file:
                    log_text = str(date) + ", " + str(url) + ", " + str(e) + "\n"
                    err_file.write(log_text)
                self.browser.quit()
                self.browser = webdriver.Firefox()
                return
        elif url:
            urls = [url]
        else:
            urls = []
        
        for article_rank, url in enumerate(urls):
            try:
                self.browser.quit()
                self.browser = webdriver.Firefox()
                self.browser.get(url)

                # remove vod bar
                self.browser.execute_script("""
                var e = document.querySelector(".vod_open");
                if (e)
                    e.parentNode.removeChild(e);
                """)

                print('crawling', url)

                print('start crawling news comment')
                cmt_list = self.browser.find_elements_by_xpath("//ul[contains(@class, 'list_comment')]//li")
                for cmt_rank, cmt in enumerate(cmt_list):
                    cmt_times = self.click_id(cmt)
                    if date is not None:
                        archive_name = '-'.join([str(date), str(article_rank+1), str(cmt_rank+1)])
                        with open('/'.join([ARCHIVE_PATH, archive_name]), 'w') as f:
                            f.write('\n'.join(cmt_times))

            except Exception as e:
                with open("error.log", 'a') as err_file:
                    log_text = str(date) + ", " + str(url) + ", " + str(e) + "\n"
                    err_file.write(log_text)

    def click_id(self, comment):
        id_btn = comment.find_element_by_css_selector("a.link_nick")
        id_btn.click()
        time.sleep(0.5)
        my_layer = self.browser.find_element_by_css_selector("div.my_layer")
        cmt_list = my_layer.find_element_by_css_selector("ul.list_comment")
        today = datetime.datetime.today()

        try:
            while True:
                # dates = my_layer.find_elements_by_css_selector("span.txt_date")
                # date_text = dates[-1].text
                last_cmt = cmt_list.find_element_by_css_selector("li:last-child")
                date_text = last_cmt.find_element_by_css_selector("span.txt_date").text
                if '분' in date_text or '시간' in date_text or '조금' in date_text: pass
                else:
                    cmt_time = datetime.datetime.strptime(date_text, "%Y.%m.%d.%H:%M")
                    time_delta = today - cmt_time
                    if time_delta.days > 6 * 30: break
                more_box = my_layer.find_element_by_css_selector("a.link_fold")
                more_box.click()
                start_time = time.time()
                while len(more_box.find_elements_by_tag_name('span')) < 2:
                    time.sleep(0.2)
                    if time.time()-start_time >= 10:
                        break
                    more_box = my_layer.find_element_by_css_selector("a.link_fold")
        except StaleElementReferenceException:
            pass

        txt_dates = my_layer.find_elements_by_css_selector("span.txt_date")
        cmt_dates = []
        for date in txt_dates:
            cmt_time_txt = date.text
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
                cmt_dates.append(str(int(cmt_time)))

        time.sleep(1)
        x_btn = my_layer.find_element_by_css_selector("a.btn_close")
        x_btn.click()
        return cmt_dates



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

    os.makedirs(ARCHIVE_PATH, exist_ok=True)

    if dt[0] == 'url':
        dc.crawl(url=dt[1])
    elif dt[0] == 'date':
        print("articles on following dates is going to be crawled: ")
        for d in dt[1]:
            print(d, end=', ')
        print("")
        for d in dt[1]:
            dc.crawl(date=d)
