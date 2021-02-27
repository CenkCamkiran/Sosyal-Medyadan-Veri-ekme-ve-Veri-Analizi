import tweepy #bu twitter için lazım
from tkinter import *
from time import sleep
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib


'''***********************Kaynak Site*****************************'''
'''https://medium.freecodecamp.org/basic-data-analysis-on-twitter-with-python-251c2a85062e'''


consumer_key = 'LPH0L9EiAqu3FXnvQy0Xq4SKF'
consumer_secret = '8Q8HiXvmRNuuEXnRjDvVZ0IiOTBhIAAnK1N5WvIWiGPD3e13on'
access_token = '3579083903-t4okeoGUePtVeDAez59xnK4JeHijv1pOHXMBiE5'
access_token_secret = 'zBUZYiWRbq8nE6OJa0takiK5Y3fvLovZiSerrEX2c2Dpp'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

wiki = TextBlob("Python is a high-level, general-purpose programming language.")

#GUI
root = Tk()

label1 = Label(root, text="Search")
E1 = Entry(root, bd =5)

label2 = Label(root, text="Sample Size")
E2 = Entry(root, bd =5)

def getE1():
    return E1.get()

def getE2():
    return E2.get()

def getData():
    getE1()
    keyword = getE1()

    getE2()
    numberOfTweets = getE2()
    numberOfTweets = int(numberOfTweets)

    #Where the tweets are stored to be plotted
    polarity_list = []
    numbers_list = []
    number = 1

    for tweet in tweepy.Cursor(api.search, keyword, lang="en").items(numberOfTweets):
        try:
            analysis = TextBlob(tweet.text)
            analysis = analysis.sentiment
            polarity = analysis.polarity
            polarity_list.append(polarity)
            numbers_list.append(number)
            number = number + 1

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    #Plotting
    axes = plt.gca()
    axes.set_ylim([-1, 2])

    plt.scatter(numbers_list, polarity_list)

    averagePolarity = (sum(polarity_list))/(len(polarity_list))
    averagePolarity = "{0:.0f}%".format(averagePolarity * 100)
    time  = datetime.now().strftime("At: %H:%M\nOn: %d-%m-%y")

    plt.text(0, 1.25, "Average Sentiment:  " + str(averagePolarity) + "\n" + time, fontsize=12, bbox = dict(facecolor='none', edgecolor='black', boxstyle='square, pad = 1'))

    plt.title("Sentiment of " + keyword + " on Twitter")
    plt.xlabel("Number of Tweets")
    plt.ylabel("Sentiment")
    plt.show()

submit = Button(root, text ="Submit", command = getData)

label1.pack()
E1.pack()
label2.pack()
E2.pack()
submit.pack(side =BOTTOM)

root.mainloop()

root = Tk()

label1 = Label(root, text="Search")
E1 = Entry(root, bd =5)

#sample size or number of tweets to be analyzed
label2 = Label(root, text="Sample Size")
E2 = Entry(root, bd =5)

submit = Button(root, text ="Submit", command = getData)

label1.pack()
E1.pack()

label2.pack()
E2.pack()

submit.pack(side =BOTTOM)

root.mainloop()
