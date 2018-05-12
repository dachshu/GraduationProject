import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import FileRW

class TweetCrawelr:
    def __init__(self):
        #self.browser = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe')
        os.environ['MOZ_HEADLESS'] = '1'
        self.browser = webdriver.Firefox()
        self.base_url = u'http://twitter.com/search?'
        self.fileRW = FileRW.FileRW()
        
    def update(self):
        # accounts = [(account, last_year, last_month), ...] tuple list
        accounts = self.fileRW.get_all_account()
        print(len(accounts))
        for account in accounts:
            self.crawling(account[0], int(account[1]), int(account[2]))



    def crawling(self, account, join_year, join_month):
        
        today_year = datetime.today().year
        today_month = datetime.today().month

        year = join_year
        month = join_month

        while True:
            tweets = []
            query = ""

            fin = False
            if(year == today_year and month == today_month):
                if month == 12 :
                    query = 'q=from%3A%40' + account + '%20since%3A' + str(year) + '-' + str(month) + '-01' + '%20until%3A'+ str(year + 1) + '-01-02&src=typd'
                else:
                    query = 'q=from%3A%40' + account + '%20since%3A' + str(year) + '-' + str(month) + '-01' + '%20until%3A'+ str(year) + '-' + str(month+1) + '-02&src=typd'
                fin = True 
            else:
                if month == 12 :
                    query = 'q=from%3A%40' + account + '%20since%3A' + str(year) + '-' + str(month) + '-01' + '%20until%3A'+ str(year + 1) + '-01-01&src=typd'
                else:
                    query = 'q=from%3A%40' + account + '%20since%3A' + str(year) + '-' + str(month) + '-01' + '%20until%3A'+ str(year) + '-' + str(month+1) + '-01&src=typd'

            url = self.base_url + query
            self.browser.get(url)
            time.sleep(1)

            prev_min_position = ""
            try:
                while True:
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    stream_container = self.browser.find_element_by_class_name('stream-container')
                    cur_min_position = stream_container.get_attribute('data-min-position')
                    if prev_min_position == cur_min_position: break
                    prev_min_position = cur_min_position

                unix_times = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]//parent::div//preceding-sibling::div[contains(@class,'stream-item-header')]//span[contains(@class,'_timestamp')]")
                tweet_texts = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]")
                tweet_ids = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]//parent::div//parent::div//parent::div[contains(@class,'js-stream-tweet')]") 
                for unix_time, tweet_text, tweet_id in zip(unix_times, tweet_texts, tweet_ids):
                    tweet = (tweet_id.get_attribute("data-tweet-id"), unix_time.get_attribute("data-time"), tweet_text.get_attribute("outerHTML"))
                    tweets.append(tweet)

                ########################
                #저장# account, list, year, month 넘겨줘야 한다
                #A.write(account, tweets, year, month)
                self.fileRW.write_tweet_list(account, tweets, year, month)
                ########################
            except NoSuchElementException: pass

            month += 1
            if month == 13: 
                year += 1
                month = 1
    
            if fin: break

    def filtering(self, account, form):
        self.fileRW.filter_tweets(account, form)
