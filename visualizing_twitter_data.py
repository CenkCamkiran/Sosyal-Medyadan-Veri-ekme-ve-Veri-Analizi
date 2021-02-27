from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


'''***********************Kaynak*****************************'''
'''YouTube Video: https://www.youtube.com/watch?v=rhBZqEWsZU4'''

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        #analysis de bunları ne olduğunu anlatmıştık. id, source bilgilerini alıp ekrana bastırmıştık
        #şimdi bu verileri grafiğe dökeceğiz.

        return df


if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)

    # print(dir(tweets[0]))
    # print(tweets[0].retweet_count)

    df = tweet_analyzer.tweets_to_data_frame(tweets)

    #grafik üzerinde veri analizine geçmeden önce numpy kütüphanesi kullanarak çekilen tweetler
    #üzerinden bazı hesaplamalar yapabiliriz.

    # Get average length over all tweets:
    # ilgili kişinin (realDonaldTrump) 20 tweetinin ortalama uzunluğunu ekrana yazdırır.
    #yukarıda count 20 yazıyor
    #'len' column un ortalamsını hesaplamamız lazım. hangi column la işlem yapıcaksak onu yazcaz ve max min vb. işlem yapıcaz
    print("(realDonaldTrump) kullanıcısından çekilen 20 tweetinin ortalama uzunluğunu: ",  np.mean(df['len']))

    #ilgili kişinin (realDonaldTrump) en çok beğenilmiş olan tweetinin like sayısını ekrana bastırır.
    # Get the number of likes for the most liked tweet:
    print("(realDonaldTrump) kullanıcısından çekilen 20 tweet arasında en çok beğenilmiş olan tweetinin like sayısı: ",  np.max(df['likes']))

    # ilgili kişinin (realDonaldTrump) tweetleri arasında en çok retweet edilen tweetin retweet sayısını ekrana yazdırır.
    # Get the number of retweets for the most retweeted tweet:
    print("(realDonaldTrump) kullanıcısından çekilen 20 tweet arasında en çok retweet edilen tweetin retweet sayısı: ",  np.max(df['retweets']))

    # ilgili kişinin (realDonaldTrump) en az beğenilmiş olan tweetinin like sayısını ekrana bastırır.
    print("(realDonaldTrump) kullanıcısından çekilen 20 tweet arasında en az beğenilmiş olan tweetinin like sayısı: ",  np.min(df['likes']))

    # print(df.head(10))


    #Time Series
    #realDonaldTrump adlı kullanıcının hergün kaç karakter tweet attığını grafiğe bastırabiliriz.
    #time_likes = pd.Series(data=df['len'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), color='r')
    #plt.show()

    #realDonaldTrump adlı kullanıcının hergün kaç like aldığını ya da bazı belirli günlerde kaç like aldığını grafiğe bastırcaz
    #pandas kütüphanesi ile realDonaldTrump adlı kullanıcının hergün kaç like aldığını ya da bazı belirli günlerde kaç like aldığını
    #hesaplamalar yapıp sistematik bir sonuç üretiyor.
    #bu sonucu da matplotlib kütüphanesi ile grafiğe dökeceğiz
    #parametre olarak bir 'likes aldı', bir de 'date' aldı. Date lere göre like sayısını hesaplayıp sonucu üretcez ve
    #matplotlib ile grafiğe bastırcaz
    #grafikte x ekseni tarihleri, y ekseni like sayısını gösteriyor
    #bazı tarihlerde fazla, bazı tarihlerde az.
    # time_favs = pd.Series(data=df['likes'].values, index=df['date'])
    # time_favs.plot(figsize=(16, 4), color='r') #grafiğin büyüklüğü ve rengi ayarlanır
    # plt.show()

    # realDonaldTrump adlı kullanıcının hergün tweetlerinin kaç kez retweet edildiği ya da bazı belirli günlerde
    # kaç kez retweet edildiğini grafiğe bastırcaz
    # pandas kütüphanesi ile realDonaldTrump adlı kullanıcının hergün tweetlerinin kaç kez retweet edildiği ya da bazı belirli günlerde
    # kaç kez retweet edildiği hakkında hesaplamalar yapıp sistematik bir sonuç üretiyor.
    # bu sonucu da matplotlib kütüphanesi ile grafiğe dökeceğiz
    # parametre olarak bir 'retweets aldı', bir de 'date' aldı. Date lere göre retweets sayısını hesaplayıp sonucu üretcez ve
    # matplotlib ile grafiğe bastırcaz
    #grafikte x ekseni tarihleri, y ekseni retweet sayısını gösteriyor
    #bazı tarihlerde fazla, bazı tarihlerde az.
    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), color='r') #grafiğin büyüklüğü ve rengi ayarlanır
    #plt.show()

    # Layered Time Series:
    #burada ise hem retweet sayısını hem like sayısını aynı grafik üzerine bastıracağız.
    #bakıldığı zaman like sayısı retweet sayısından hep fazla grafiğe göre
    '''time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="likes", legend=True) # lejant ekledik. likes yazdık
    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_retweets.plot(figsize=(16, 4), label="retweets", legend=True) #lejant ekledik. retweets yazdık

plt.show()'''