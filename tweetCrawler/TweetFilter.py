from bs4 import BeautifulSoup
import re

class TweetFilter:
    def textFiltering(self, tweets):
        texts = []
        ptn = re.compile(r'<p .+>.+</p>')
        for tweet in tweets:
            tweet = ptn.search(tweet).group(0)
            soup = BeautifulSoup(tweet, 'html.parser')
            u_hidden = soup.findAll('a', {"class" : "u-hidden"})
            for element in u_hidden: element.extract()
            texts.append(re.sub(r'\n{2,}','\n',soup.get_text()) + '\n\n')
        return texts

    def timeFiltering(self, tweets):
        times = []
        ptn = re.compile(r'(\d+)\n(\d+)\n')
        for tweet in tweets:
            times.append(ptn.search(tweet).group(2) + '\n')
        return times

    def filtering(self, tweets, form):
        if form == 'text': return self.textFiltering(tweets)
        elif form == 'time': return self.timeFiltering(tweets)
        else: return None
