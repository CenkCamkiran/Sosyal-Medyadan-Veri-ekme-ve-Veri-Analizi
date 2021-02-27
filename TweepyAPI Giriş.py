import tweepy #bu twitter için lazım
from tkinter import *
from time import sleep
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib


'''***********************Kaynak Site*****************************'''
'''http://docs.tweepy.org/en/v3.5.0/'''


consumer_key = 'LPH0L9EiAqu3FXnvQy0Xq4SKF'
consumer_secret = '8Q8HiXvmRNuuEXnRjDvVZ0IiOTBhIAAnK1N5WvIWiGPD3e13on'
access_token = '3579083903-t4okeoGUePtVeDAez59xnK4JeHijv1pOHXMBiE5'
access_token_secret = 'zBUZYiWRbq8nE6OJa0takiK5Y3fvLovZiSerrEX2c2Dpp'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)


#**********************************************Status Methods**********************************************
#Update the authenticated user’s status. Statuses that are duplicates or too long will be silently ignored.
# Sample method, used to update a status tweet yolluyor!
'''api.update_status('Hello Python Central! #pythoncentral')'''


# Returns the authenticated user’s information.
user = api.me()
#bilgileri yazdır. json verisi
'''print(user)'''


#3579083903 user id
'''print('Ad: ' + user.name)
print('Konum: ' + user.location)
print('Takip Edilenler: ' + str(user.friends_count))'''

'''print (user.screen_name)
print (user.followers_count) #takipçi sayısı
for friend in user.friends():
   print (friend.screen_name) #takip edilenleri ekrana bastırır'''


#Resim paylaşır(Tweet)
'''api.update_with_media('C:/Users/Cenk/Desktop/Setup/ssaddsa.jpg', 'Cenk', in_reply_to_status_id = 1058040341822128134)'''


#The ID of an existing status that the update is in reply to.(Cevap Yollar)
'''api.update_status('Cenk', in_reply_to_status_id = 1057947752590729222)'''


#Destroy the status specified by the id parameter. The authenticated user must be the author of the status to destroy.
#ana twiti siler. cevapları silmez
'''api.destroy_status(1058040341822128134)'''


#twit id yi alıp retweetler
#Retweets a tweet. Requires the id of the tweet you are retweeting.
'''api.retweet(1058040614959439874)'''


#json verisi geri döndürür. verilen tweetin id si ile bilgilerini ekrana bastırabilirsin
#Returns a single status specified by the ID parameter.
'''status = api.get_status(1058036591808208898)
print(status.created_at)'''

#**********************************************Timeline Methods**********************************************
#Returns the 20 most recent statuses, including retweets, posted by the authenticating user and that user’s friends
'''public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)'''


'''result = api.statuses_lookup([1057963156331466752, 1057962235832778752]) #tek tırnak da kabul
for tweet in result:
    print(tweet.text) #verilen tweet id lerini alarak içeriklerini ekrana bastırıyor (MAX 100 tane)'''


#Returns the 20 most recent tweets of the authenticated user that have been retweeted by others.
'''retweets = api.retweets_of_me();
for tweet in retweets:
    print(tweet.text)'''


#Returns the 20 most recent statuses posted from the authenticating user or the user specified.
# It’s also possible to request another user’s timeline via the id parameter.
'''sonuc = api.user_timeline(783214)
for tweet in sonuc:
    print(tweet)'''


#**********************************************User Methods**********************************************
# Get the User object for twitter...
#Returns information about the specified user.
'''user = api.get_user('Twitter')
print(user.id)'''


#Returns an user’s followers ordered in which they were added 100 at a time.
#If no user is specified by id/screen name, it defaults to the authenticated user.
'''followers = api.followers('Twitter')
print(followers)'''


#statuses_count tweet sayısı
#Returns information about the specified user.
#id ya da screen name girilir.
'''kullanıcı = api.get_user(783214)
print(kullanıcı.statuses_count)'''


#Run a search for users similar to Find People button on Twitter.com; the same results returned by people search on Twitter.com will be returned by using this API (about being listed in the People Search).
# It is only possible to retrieve the first 1000 matches from this API.
#page ile pagination yapılır
'''result = api.search_users('giraffe', page = 2)
print(result)'''


#Returns up to 100 of the first retweets of the given tweet.
'''information = api.retweets(1057983433383862272, count=100)
print(information)'''#buna bak


#**********************************************Favourite Methods**********************************************
#Returns the favorite statuses for the authenticating user or user specified by the ID parameter.
#Specifies the page of results to retrieve
#pagination ile sayfalar arasında gezinir
'''favs = api.favorites('ShalamanDay23', page=1)
for tweet in favs:
    print(tweet.text)'''


#Favorites the status specified in the ID parameter as the authenticating user.
#Tweeti beğenir
'''api.create_favorite(1058040614959439874)'''


#Un-favorites the status specified in the ID parameter as the authenticating user.
#Tweeti beğenmeyi bırakır
'''api.destroy_favorite(1058040614959439874)'''


#**********************************************Trends Methods**********************************************

#Returns the locations that Twitter has trending topic information for.
#The response is an array of “locations” that encode the location’s WOEID (a Yahoo! Where On Earth ID) and some other human-readable information such as a canonical name
#and country the location belongs in.
'''trends = api.trends_available()
for tweet in trends:
    print(tweet)'''


#Returns the top 10 trending topics for a specific WOEID, if trending information is available for it.
#The response is an array of “trend” objects that encode the name of the trending topic, the query parameter that can be used to search for the topic on Twitter Search, and the Twitter Search URL.
#This information is cached for 5 minutes. Requesting more frequently than that will not return any more data, and will count against your rate limit usage.
'''place = api.trends_place(2972)
for trend in place:
    print(trend)'''


#**********************************************Friendship Methods**********************************************

#Create a new friendship with the specified user (aka follow).
#screen name ya da id girilebilir.
'''api.create_friendship('XTheWitcherX')'''


#Destroy a friendship with the specified user (aka unfollow).
'''api.destroy_friendship('XTheWitcherX')'''

#Returns an array containing the IDs of users being followed by the specified user.
#belirtilen kullanıcı tarafından takip edilen kişilerin id lerini döndürüyor.
'''friends = api.friends_ids('ShalamanDay23')
print(friends)'''

#Returns an array containing the IDs of users following the specified user.
#belirtilen kullanıcıyı takip eden kullanıcıların id lerini geri döndürür.
'''friends = api.followers_ids('ShalamanDay23')
print(friends)'''