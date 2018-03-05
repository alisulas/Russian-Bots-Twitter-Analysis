import csv
import json
from pprint import pprint
from pymongo import MongoClient

columns = [
    "user_id",              # int
    "user_key",             # string : screen name
    "created_at",           # timestamp
    "created_str",          # string: created_at timestamp 
    "retweet_count",        # int
    "retweeted",            # boolean
    "favorite_count",       # int
    "text",                 # string
    "tweet_id",             # int
    "source",
    "hashtags",             # string[]
    "expanded_urls",        # string[]
    "mentions",             # string[]
    "retweeted_status_id",  # int
    "in_reply_to_status_id" # int
]

if __name__ == '__main__':
    client = MongoClient("localhost", 27017, maxPoolSize=50)
    db = client.twitter
    collection = db.tweet
    cursor = collection.find({})
    with open("scraped_tweets.csv", "w") as outfile:
        fields = columns
        write = csv.DictWriter(outfile, fieldnames = fields)
        write.writeheader()
        for row in cursor:
            # pprint(row)
            # print("\n\n")
            try:
                full_text = row["retweeted_status"]["extended_tweet"]["full_text"]
            except:
                full_text = row['text']

            hashtags = [elem['text'] for elem in row['entities']['hashtags']]
            urls     = [elem['expanded_url'] for elem in row['entities']['urls']]
            mentions = [elem['screen_name'] for elem in row['entities']['user_mentions']]

            flattened_record = {
              "user_id"              : row['id'],
              "user_key"             : row['user']['screen_name'],
              "created_at"           : row['timestamp_ms'],
              "created_str"          : row['created_at'],
              "retweet_count"        : row['retweet_count'],
              "retweeted"            : row['retweeted'],
              "favorite_count"       : row['favorite_count'],
              "text"                 : full_text,
              "tweet_id"             : row['id'],
              "source"               : row.get('source', ''),
              "hashtags"             : hashtags,
              "expanded_urls"        : urls,
              "mentions"             : mentions,
              # "retweeted_status_id"  : row["retweeted_status"]["id"],
              "retweeted_status_id"  : row.get('retweeted_status', {}).get('id'),
              "in_reply_to_status_id": row['in_reply_to_status_id']
            }

            write.writerow(flattened_record)

