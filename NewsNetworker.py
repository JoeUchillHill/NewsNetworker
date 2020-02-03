import tweepy
import csv
import time
import timeit
import datetime
import re


def tweetrate (listoftweets):
    #Takes a list of tweets of type tweepy.cursor(api.user_timeline,...), returns [rate of tweets in tweets per day (including fractional), total number of tweets in dataset, and the time period of the sample as a timedelta]
    tweet = []
    for tweet1 in listoftweets:
        tweet.append(tweet1.created_at)
    length = len(tweet)
    datebegin = tweet[0]
    dateend = tweet[length-1]
    return [(length-1)/((datebegin-dateend).days + (datebegin-dateend).seconds/86400), length, datebegin-dateend]

def maybe_enum (list, keep="off"):
    #Checks to see which of a list of user names end in a sequence of numbers, possibly indicating that a username was automatically generated in sequence.
    #
    #An example of this might be a number of accounts that look like "chair02003", "book20031", "world60063" - a clear pattern of words followed by 5 digit sequences.
    #Of course, there are a bunch of reasons people put numbers in their names organicaly-- "Trump2020". "SexySince1979". "n1ckn4m3", etc.
    #
    #By default, maybe_enum returns a 2d list where list[x] = [user name, digit at end of username], ignoring all usernames that don't end in digits.
    #If the variable 'keep' is set to "on" - i.e., calling it as maybe_enum(list,"on") - it won't ignore the usernames that don't end in digits, but instead handle those like this: ["nodigit", -1]
    outlist = []
    for user in list:
        enum = re.search(r'\d+$', user)
        if enum is not None:
            outlist.append([user, enum.group()])
        else:
            if keep == "on":
                outlist.append([user, -1])
    return outlist

def enum_sort (enums):
    #maybe you'd rather see your "maybe_enum" list in terms of how many names ended in sequences of digits of length (n). This will do that! Every outlist [n] = [total number of usernames ending in a sequence of length n, list of names fitting that criteria] 
    outlist = [[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]]]
    for userstat in enums:
        outlist[len(userstat[1])][1].append(userstat[0])
        outlist[len(userstat[1])][0] =  outlist[len(userstat[1])][0] + 1
    return outlist


def hasfollowers (user, thresh = 1):
    #takes a user of type api.get_user(user) and checks if it has at least 'thresh' number of followers. If no thresh is given, defaults to 1
    if user.friends_count > thresh:
        return (0)
    else:
        return (1)   
    
def hastweeted (listoftweets, thresh=1):
    #Takes a list of tweets of type tweepy.Cursor(api.user_timeline...) and tells you if the account has tweeted at least thresh times (thresh defaults to 1
    tweet = []
    for tweet1 in listoftweets:
        tweet.append (tweet1)
    if len(tweet) > thresh:
        return (1)
    else:
        return (0)

 def rate_limiter(api):
    #This function checks if you've hit any twitter API limits. If you have, this module will pause your program until the limits reset,
    #checking every 60 seconds to see if they have. 
         # DUMMY CODE FOR TWEEPY ERROR HANDLING
         #try:
              # [Tweepy API Call]
         #except tweepy.error.RateLimitError:
         #    rate_limit_check()
    rate_limit = api.rate_limit_status()["resources"]
    while true:    
        for rate in rate_limit:
            endpoints = rate_limit[rate]
            for endpoint in endpoints:
                limit = rate_limit[rate][endpoint]["limit"]
                remaining = rate_limit[rate][endpoint]["remaining"]
                if remaining == 0:
                    time.sleep(60)
                else return

