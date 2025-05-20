import os
import sys
import tweepy
import shutil
import pathlib
import json
from datetime import date
from dotenv import load_dotenv

load_dotenv()
openConfig = open("./config.json")
loadedConfig = json.load(openConfig)
inTestingMode = loadedConfig['TestingMode']
# print(f"inTestingMode Type == {type(inTestingMode)}")
# print(f"inTestingMode == {inTestingMode}")

def postToTwitterX():
    # Following a medium article
    ACCESS_KEY = os.getenv("twitterAccessKey")
    ACCESS_SECRET = os.getenv("twitterAccessSecret")
    CONSUMER_KEY = os.getenv("twitterConsumerKey")
    CONSUMER_SECRET = os.getenv("twitterConsumerSecret")
    BEARER_TOKEN = os.getenv("TwitterBearerToken")

    #authenticate to twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(
        ACCESS_KEY,
        ACCESS_SECRET,
    )
    # API V2 connect
    newapi = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        access_token=ACCESS_KEY,
        access_token_secret=ACCESS_SECRET,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
    )
    # api V1
    api = tweepy.API(auth)

    #Not in tutorial, loading json stuff
    if inTestingMode == True:
        twitterNotifFile = f"{os.getcwd()}/notifs/test.json"
    else:
        twitterNotifFile = f"{os.getcwd()}/notifs/streamNotifs.json"

    # Post data
    openTwitterNotifFile = open(twitterNotifFile)
    loadedTwitterNotif = json.load(openTwitterNotifFile)
    streamNotif = f"""{loadedTwitterNotif["Line1"]}
{loadedTwitterNotif["Line2"]}

{loadedTwitterNotif["streamLink"]}
{loadedTwitterNotif["hashtags"]}"""

    # create the tweet using the new api. Mention the image uploaded via the old api
    post_result = newapi.create_tweet(text=streamNotif)
    # the following line prints the response that you receive from the API. You can save it or process it in anyway u want. I am just printing it.
    print(post_result)
    exit("Posted on twitter")