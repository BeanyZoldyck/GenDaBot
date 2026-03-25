import pandas as pd
import os
import snscrape.modules.twitter as sntwitter
from tweety.bot import Twitter
normalize = lambda y: ' '.join(i for i in filter(lambda x: ('@' not in x) and ('https://' not in x),y.split()))

profiles = 'JozuJoestar crackcobain__ 222corn ayeejuju adam22 tarrasq__e Vuetzel'

for profile in profiles.split():
    print(f"Scraping {profile}")
    scraper = sntwitter.TwitterProfileScraper(profile)
    with open(f'man\\{profile}.txt','ab') as prof:
        for tweet in scraper.get_items():
            try:
                raw = tweet.rawContent
                if raw[:2] != 'RT':
                    prof.write(bytes(normalize(raw),'utf-8')+b'\n')
            except AttributeError:
                pass
        prof.close()
'''
app = Twitter()
for profile in profiles.split():
    all_tweets = app.get_tweets(profile)
    for tweet in all_tweets:
      input(tweet)
'''
