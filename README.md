# gallery-dl-orphan-parent-grabber
This script is intended for use after using gallery-dl (https://github.com/mikf/gallery-dl) to scrape a twitter profile for text tweets including replies. Getting very old tweets is difficult due to the twitter API rate limit and the need to step through all tweets backwards every time you run gallery-dl. This script takes a directory full of JSON files for tweets by a given user and generates a command to download each missing parent tweet individually.

If you have 1 file:

`1234567890123456789-TwitterSupport.json`
```
{
  "tweet_id": 1234567890123456789,
  "reply_id": 9876543210987654321,
  "reply_to": "UserInDistress"
}
```

this results in the following command if the file "9876543210987654321-UserInDistress.json" is not found in the same directory:

`gallery-dl.exe https://twitter.com/UserInDistress/status/9876543210987654321`
