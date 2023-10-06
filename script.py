import os
import glob
import json

# This script is intended for use after using gallery-dl (https://github.com/mikf/gallery-dl) to scrape a twitter profile for text tweets including replies
# Getting very old tweets is difficult due to the twitter API rate limit and the need to step through all tweets backwards every time you run gallery-dl
# This script takes a directory full of JSON files for tweets by a given user and generates a command to download each missing parent tweet individually
# If you have 1 file called "1234567890123456789-TwitterSupport.json" and that tweet was a reply to "UserInDistress", this results in the following command
# if the parent file is not found in the same directory
# gallery-dl.exe https://twitter.com/UserInDistress/status/9876543210987654321

###
### Before Use:
### Update TWEET_DIR_PATH to the folder containing your tweets folder
### Update USERNAME to the handle of the child account
### Update COMMANDS_FILEPATH to a destination file. The commands will be added to this file
### Double-check line 56 and make sure the search terms match your filename pattern. Currently it searches for files that look like "*1234567890123456789-TwitterSupport*.json"
###
# TWEET_DIR_PATH = r"P:\ath\to\tweets\folder\tweets"
TWEET_DIR_PATH = r""
# COMMANDS_FILEPATH = "P:\ath\to\batch\file.bat"
COMMANDS_FILEPATH = ""
# USERNAME = "TwitterSupport"
USERNAME = ""

def addCommandToFile(text):
  with open(COMMANDS_FILEPATH, "a", encoding="utf-8") as file:
    file.write(f"{text}\n")

def findOldReplies(directory):
  if not TWEET_DIR_PATH or not os.path.exists(TWEET_DIR_PATH):
    print(f"Directory '{TWEET_DIR_PATH}' does not exist")
    return

  if not COMMANDS_FILEPATH or not os.path.isfile(COMMANDS_FILEPATH):
    print(f"File '{COMMANDS_FILEPATH}' does not exist")
    return

  if not USERNAME:
    print("USERNAME is not set")
    return

  json_files = glob.glob(os.path.join(directory, '*.json'))

  for filepath in json_files:
    filename = os.path.basename(filepath)
    if USERNAME in filename:
      try:
        with open(filepath, "r", encoding='utf-8') as file:
          data = json.load(file)
          # reply_id will be 0 if the tweet was not a reply
          if "reply_id" in data and int(data["reply_id"]) > 0:
            replyId = data["reply_id"]
            replyTo = data["reply_to"]
            # Checks if a file already exists with this id and handle. Change this bit to fit your pattern
            fileFound = [filename for filename in json_files if f"{replyId}-{replyTo}" in filename]
            tweetUrl = f"https://twitter.com/{replyTo}/status/{replyId}"
            if not fileFound:
              command = f"gallery-dl.exe {tweetUrl}"
              addCommandToFile(command)
          elif not "reply_id" in data:
            print(f"'reply_id' field not found in {filepath}")
      except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")

findOldReplies(TWEET_DIR_PATH)
