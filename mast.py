import os
import sys
import shutil
import pathlib
import json
from datetime import date
from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()
openConfig = open("./config.json")
loadedConfig = json.load(openConfig)
inTestingMode = loadedConfig['TestingMode']
# print(type(inTestingMode))
# print(inTestingMode)

if loadedConfig['postingTo']['mastodon'] == True:
    api = os.getenv("mastApiUrl")
    MastAccessToken = os.getenv("mastAccessToken")
    #Not in tutorial, loading json stuff
    if inTestingMode == True:
        mastNotifFile = f"{os.getcwd()}/notifs/test.json"
    else:
        mastNotifFile = f"{os.getcwd()}/notifs/streamNotifs.json"

    # Post data
    openmastNotifFile = open(mastNotifFile)
    loadedmastNotif = json.load(openmastNotifFile)
    streamNotif = f"""{loadedmastNotif["Line1"]}
{loadedmastNotif["Line2"]}

{loadedmastNotif["streamLink"]}
{loadedmastNotif["hashtags"]}"""
    print(streamNotif)

    mastodonToot = Mastodon(access_token = MastAccessToken, api_base_url = api)
    mastodonToot.toot(streamNotif)

    exit(f"Posted on mastodon ({api})")
else:
    print("Posting to mastodon is disabled in ./config.json, skipping!")