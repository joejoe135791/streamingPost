import os
import sys
import shutil
import pathlib
import json
from datetime import date
from dotenv import load_dotenv
from atproto import Client

load_dotenv()
openConfig = open("./config.json")
loadedConfig = json.load(openConfig)
inTestingMode = loadedConfig['TestingMode']
# print(type(inTestingMode))
# print(inTestingMode)

def postToBluesky():
    client = Client()
    # Login
    bskyLoginUsername = os.getenv("bskyUsername")
    bskyLoginAppPassword = os.getenv("bskyAppPassword")
    client.login(f'{bskyLoginUsername}', f'{bskyLoginAppPassword}')

    # loading json stuff
    if inTestingMode == True:
        bskyNotifFile = f"{os.getcwd()}/notifs/test.json"
    else:
        bskyNotifFile = f"{os.getcwd()}/notifs/streamNotifs.json"

    # post data
    openbskyNotifFile = open(bskyNotifFile)
    loadedBskyNotif = json.load(openbskyNotifFile)
    streamNotif = f"""{loadedBskyNotif["Line1"]}
{loadedBskyNotif["Line2"]}

{loadedBskyNotif["streamLink"]}
{loadedBskyNotif["hashtags"]}"""

    # send to bsky
    print(streamNotif)
    client.send_post(text=streamNotif)
    print("Posted to Bsky (bsky.app)")