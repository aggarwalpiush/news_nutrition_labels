import twitter
import tldextract


class ExtractAuthFeatures(object):

    debug = False

    def __init__(self):
        self.consumer_key = "firgrfdffhgfdecjlkinnkjbhiedrhvi"
        self.consumer_secret = "lkhbjudevbtjjlifhtljltvulhlfbfjg"
        self.access_token = "gknbifhujudfdjenktgigfivetcggtcc"
        self.access_token_secret = "rvffjeubucngckdhlublteteinitjjuh"
        self.url_domain = []

    def get_source(self, url):
        news_source = tldextract.extract(url)
        if news_source.domain in self.url_domain:
            return None
        else:
            self.url_domain.append(news_source.domain)
            return news_source.domain

    def get_tweets(self, news_source):
        authent = twitter.Twitter(auth=twitter.OAuth(self.access_token, self.access_token_secret,
                                                     self.consumer_key, self.consumer_secret))
        results = authent.users.search(q=news_source)
        twit_user = {}
        if len(results) >= 1:
            for user in results:
                twit_user['followers_count'] = user['followers_count']
                twit_user['friends_count'] = user['followers_count']
                twit_user['listed_count'] = user['listed_count']
                twit_user['favourites_count'] = user['favourites_count']
                break
        else:
            twit_user['followers_count'] = 0
            twit_user['friends_count'] = 0
            twit_user['listed_count'] = 0
            twit_user['favourites_count'] = 0
        return twit_user
