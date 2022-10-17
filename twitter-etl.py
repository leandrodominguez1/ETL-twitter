import tweepy
import json
from datetime import datetime 
import s3fs
from secrets_keys import api_key, api_secrets, access_token, access_secret, bearer_token
import pandas as pd

# Twitter authentication
auth = tweepy.OAuthHandler(api_key, api_secrets)   
auth.set_access_token(access_token, access_secret) 

# # # Creating an API object 

account = 'JeffBezos'

api = tweepy.API(auth)
tweets = api.user_timeline(screen_name='@{}'.format(account), 
                        # 200 is the maximum allowed count
                        count=150,
                        include_rts = False,
                        # Necessary to keep full_text 
                        # otherwise only the first 140 words are extracted
                        tweet_mode = 'extended',
                        )

tweets_list = []

for tweet in tweets:
    text = tweet._json['full_text']

    refined_tweet = {'user': tweet.user.screen_name,
                     'text': text,      
                     'favorite_count': tweet.favorite_count,
                     'retweet_count': tweet.retweet_count,
                     'created_at': tweet.created_at
                    }

    tweets_list.append(refined_tweet)

df = pd.DataFrame(tweets_list)
df.to_csv('{}_data_tweets.csv'.format(account)) 



