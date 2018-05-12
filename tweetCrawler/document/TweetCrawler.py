import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TweetCrawelr:
    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe')
        self.base_url = u'http://twitter.com/'
        
    def update(self, account, last_tweetid):
         ret_data = []
         query = account
         url = self.base_url + query
         self.browser.get(url)
         time.sleep(0.2)

         while True:
             self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
             time.sleep(1)
             end_el = self.browser.find_element_by_class_name('stream-end')
             tweetids = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]//parent::div//parent::div//parent::div[contains(@class,'js-stream-tweet')]")
             cur_ti = str()
             if tweetids[len(tweetids) - 1].get_attribute("data-retweet-id"): cur_ti = tweetids[len(tweetids) - 1].get_attribute("data-retweet-id")
             else: cur_ti = tweetids[len(tweetids) - 1].get_attribute("data-tweet-id")
             if last_tweetid >= int(cur_ti) : break

         tweetids = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]//parent::div//parent::div//parent::div[contains(@class,'js-stream-tweet')]")
         tweets = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]")
         usernames = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]//parent::div//preceding-sibling::div[contains(@class,'stream-item-header')]//span[contains(@class,'username')]")

         for tweetid, tweet, username in zip(tweetids, tweets, usernames):
             tid = str()
             if tweetid.get_attribute("data-retweet-id"): tid = tweetid.get_attribute("data-retweet-id")
             else: tid = tweetid.get_attribute("data-tweet-id")
             if(int(tid) <= last_tweetid): break
             if(username.text == '@' + account):                 
                 tp = (int(tid),tweet.get_attribute("outerHTML"))
                 ret_data.append(tp)

         return ret_data



    def crawling(self, account):
         ret_data = []
         query = account
         url = self.base_url + query
         self.browser.get(url)
         time.sleep(0.2)

         while True:
         #for i in range(2):
             self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
             time.sleep(1)
             end_el = self.browser.find_element_by_class_name('stream-end')
             if end_el.is_displayed(): break

         tweetids = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]//parent::div//parent::div//parent::div[contains(@class,'js-stream-tweet')]")
         tweets = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]")
         usernames = self.browser.find_elements_by_xpath("//p[contains(@class,'tweet-text')]//parent::div//preceding-sibling::div[contains(@class,'stream-item-header')]//span[contains(@class,'username')]")

         for tweetid, tweet, username in zip(tweetids, tweets, usernames):
             if(username.text == '@' + account):
                 tid = str()
                 if tweetid.get_attribute("data-retweet-id"): tid = tweetid.get_attribute("data-retweet-id")
                 else: tid = tweetid.get_attribute("data-tweet-id")
                 tp = (int(tid),tweet.get_attribute("outerHTML"))
                 ret_data.append(tp)

         return ret_data



    def crawl(self, account, exist, last_tweetid):
        if(exist): return self.update(account, last_tweetid)
        else: return self.crawling(account)


'''
t = TweetCrawelr()
ret = t.crawl('realDonaldTrump',True, 909401572341370880)
print(len(ret))

for i in range(len(ret)):
    print(ret[i][0])
    print(ret[i][1])

print("end")
'''