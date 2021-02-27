from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pandas as pd

#pandas ı visualizing kısmında kullancaz. çektiğimiz tweet leri data frame lere atayıp  grafikle göstercez

#pandas is an open source, BSD-licensed library providing high-performance,
#easy-to-use data structures and data analysis tools for the Python programming language.

#NumPy is the fundamental package for scientific computing with Python
#Besides its obvious scientific uses, NumPy can also be used as an efficient multi-dimensional container of generic data

#numpy general-purpose numerical library for python


'''***********************Kaynak Site*****************************'''
'''# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg'''


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

#her bir tweetin bilgilerini yazdırıken tek tek comment line al göstermeyi unutma
#tweetin içeriği ve ilgili tweetin id leri ekrana yazdırıyor. üstünde göster
    def tweets_to_data_frame(self, tweets): #bu fonksiyonla wteetleri çektik, tweets e attık.
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        #bu tweets içeriğini (yani alınan tüm tweetleri) döngüyle geziyoruz
        #we want to extract text each of these tweets
        #döngüyle, ilgili kullanıcının her bir tweetleri gezilir. gezilen her
        #bir tweetin text alanlarını alacağız(çıkartacağız)
        #column kısmı tweets. çünkü biz bu çekilen her bir tweetin text alanalrını aldık.
        #bu çekilen veriler data frame de hangi (nerede) kısımda duracak
        # (tweets sütununun altında bu çekilen veriler duracak)

        # bu tweets içeriğini (yani alınan tüm tweetleri) döngüyle geziyoruz. döngüyle gezerken her bir tweetin bil-
        #gilerini numpy array ine atıyoruz
        df['id'] = np.array([tweet.id for tweet in tweets])
        #her bir tweetin id bilgisini alıp listeye attık(id column un altına)

        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        #her bir tweetin text bilgisinin lenght (uzunluğu) alıp listeye attık(text column un altına)

        df['date'] = np.array([tweet.created_at for tweet in tweets])
        #her bir tweetin created_at bilgisini alıp listeye attık(created_at column un altına)

        df['source'] = np.array([tweet.source for tweet in tweets])
        #her bir tweetin source bilgisini alıp listeye attık(source column un altına)
        #tweet pc'den mi, android ya da ios dan mı atılmış onun bilgisi

        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        #her bir tweetin favorite_count bilgisini alıp listeye attık(favorite_count column un altına)

        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        #her bir tweetin retweet_count bilgisini alıp listeye attık(retweet_count column un altına)

        return df


if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=20)
    #screen name'i realDonaldTrump olan kullanıcının timeline nından 20 tane tweet çekicez
    #print(tweets) burada yazılan veriler json formatında

    #print(dir(tweets[0])) #ilk tweetin bütün verilerini (bilgilerini) ekrana yazdırabiliriz.
    #aslında her bir twitten ne tür bilgiler çekebiliriz bunları bu kodla anlayabiliriz.
    #source, retweet_count, favorite_count, id, geo(nerden atıldığının koordinatları)
    #her bir tweetten bu bilgileri nasıl çıkartıcaz ve bu bilgileri nasıl dataframe koyucaz ve göstericez sorusunun cevabı
    #ise, her bir tweetin sadece içeriği değil, fav sayısı, retweet sayısı, ,id'si, nerden atıldığı, hangi twitter
    #uygulamasından atıldığı gibi bilgileri tweets_to_data_frame fonksiyonuyla, bu bilgileri bir dataframe e atıcaz ve
    #ekrana bastırcaz

    #print(tweets[0].id)
    #ilk tweeitn id bilgisini erana yazdırır.
    #index ile ilgili tweete ulaşabilirsin
    #print(tweets) #json verisi

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    #tweetlerin id, source vb. bilgilerini (fonksiyonda yazdığımız column lar)
    #tweets_to_data_frame fonksiyonu ile çektik ve df ye atadık

print(df.head(10))#ilk 10 tweet #data framedeki ilk 10 elementi yazdırcaz
#dataframe deki ilk 10 object'teki id, source, tweets, likes vb. alanları (sütunları) ekrana yazdırdık.