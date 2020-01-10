import tweepy
import csv
import time
import timeit
import datetime


def tweetrate (listoftweets):
    #Takes a list of tweets of type tweepy.cursor(api.user_timeline,...), returns [tweets per day (including fractional), total number of tweets in dataset, and the time period of the sample as a timedelta]
    tweet = []
    for tweet1 in listoftweets:
        tweet.append(tweet1.created_at)
    length = len(tweet)
    datebegin = tweet[0]
    dateend = tweet[length-1]
    return [(length-1)/((datebegin-dateend).days + (datebegin-dateend).seconds/86400), length, datebegin-dateend]
