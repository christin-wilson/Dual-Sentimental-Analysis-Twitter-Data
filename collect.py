from __future__ import absolute_import, print_function

import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="LfyfmZTKVSKzVA97V6ZBviTSw"
consumer_secret="D6yYbu3KeZ58LiSPuaMtygnXNxlS34EX5n4QrxRKKcJ5Pp8d6n"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="3593497752-38j0Z0LhWr1UBXVFtCUlPRHCsl33kbkGrPUNtxE"
access_token_secret="vMBdncbvVunRWtcZaZFtgM5r7MA6KYlY6Dy7VUcQbIRA9"

limit=5

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
text_file = open("data/abc.txt", "w")



for tweet in tweepy.Cursor(api.search, q="yandex",lang="en").items(int(limit)):
	tweets=tweet.text
	text_file.write(tweets)
	text_file.write("\n")
	


text_file.close()

