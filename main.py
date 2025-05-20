import os
import sys
import shutil
import pathlib
import json
import postLiveToBsky as pl2bsky
import postLiveToMastodon as pl2mast
import postLiveToTwitter as pl2twitter
from datetime import date
from dotenv import load_dotenv
# from atproto import Client

load_dotenv()
openConfig = open("./config.json")
loadedConfig = json.load(openConfig)
inTestingMode = loadedConfig['TestingMode']
defaultStreamLink = loadedConfig['defaultStreamLink']
newOrExistingPostAnswer = 0
streamNotifFile = f"{os.getcwd()}/notifs/streamNotifs.json"

try:
    os.mkdir('./notifs')
except FileExistsError:
    pass
except Exception as e:
    sys.exit(f"An unknown exception occurred.\n{e}")

while True:
    while True:
        try:
            print('If you are in testing mode, press 2')
            newOrExistingPostAnswer = int(input("Press 1 to create a new post or press 2 to reuse the last post: "))
            break
        except ValueError:
            print("Please enter a number!")
            newOrExistingPostAnswer = 0
        except Exception as e:
            sys.exit(f"An unknown exception occurred\n{e}")
        
    if newOrExistingPostAnswer == 1 or 2:
        break
    else:
        print(f"{newOrExistingPostAnswer} is not a valid selection")

if newOrExistingPostAnswer == 1:
    line1Msg = str(input("What should the first line say?: "))
    line2Msg = str(input("What should the second line say?: "))
    hashtagsMsg = str(input("What should the hashtags be?: "))
    streamMessage2Json = { 
        "Line1":line1Msg,
        "Line2":line2Msg,
        "streamLink":defaultStreamLink,
        "hashtags":hashtagsMsg
    }
    with open(streamNotifFile, 'w') as notifWrite:
        json.dump(streamMessage2Json, notifWrite, indent=4)

loadedNotifFile = json.load(open(streamNotifFile))
messagePreview = f"""{loadedNotifFile["Line1"]}
{loadedNotifFile["Line2"]}

{loadedNotifFile["streamLink"]}
{loadedNotifFile["hashtags"]}"""

print(f"Here is a preview of the message.\n{messagePreview}")
isItGood = input("\nIs this message okay? [y/n]: ")

if isItGood.casefold == 'y' or 'yes':
    # Bsky
    if loadedConfig['postingTo']['bluesky'] == True:
        pl2bsky.postToBluesky()
    else:
        print("Posting to Bluesky is disabled, skipping!")

    # Mast
    if loadedConfig['postingTo']['mastodon'] == True:
        pl2mast.postToMast()
    else:
        print("Posting to Mastodon is disabled, skipping!")

    # Twitter
    if loadedConfig['postingTo']['twitter'] == True:
        pl2twitter.postToTwitter()
    else:
        print("Posting to Twitter is disabled, skipping!")
    
    sys.exit("Script has finished running! Press enter to close")
else:
    sys.exit("Please rerun the script to reconfigure the message")