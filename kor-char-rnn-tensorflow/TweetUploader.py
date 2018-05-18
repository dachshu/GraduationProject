import argparse
import time
# import twitter
import sample
import DaumIssueCrawler
import time_generate


class TweetUploader:
    def __init__(self, save_dir):
        self.save_dir = save_dir
        
    
    def upload(self):
        while True:
            remaining_sec = time_generate.get_next_remaining_seconds()
            print(remaining_sec, 'sleep')
#time.sleep(remaining_sec)
            time.sleep(5)
            
            issue_crawler = DaumIssueCrawler.DaumIssueCrawler()
            issue_word = issue_crawler.get_issue_word()
            print('issue word : ' + issue_word )
            text = sample.sample(self.save_dir, issue_word)
            print('text :' + text)

            #upload
            # api = twitter.Api(consumer_key='zexHhvrrG45tSLsKQTySJ0FKG',
                    # consumer_secret='OxsUkRcArkimr6fO9TdAvjhcDfrgwvzW0YytybRMs6WNUkIAlA', 
                    # access_token_key='903173915811254272-Otqw7io4GiqOtq5LIMW8nPDOTP9EDIb',
                    # access_token_secret='0q8jbHXgNhbpsFyJnfkxJA9g0om7MW6yF0pyjagAZF8kt')
            # status = api.PostUpdate(text)
            print(text)
            time_generate.update_log()
            issue_crawler = None



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('save_dir', type=str, default='save',
                        help='model directory to store checkpointed models')

    args = parser.parse_args()

    tweet_uploader = TweetUploader(args.save_dir)
    tweet_uploader.upload()
