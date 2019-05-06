from elasticsearch import Elasticsearch
import nltk
import json
from textblob import TextBlob
import numpy as np
from redis_script import *

es = Elasticsearch()

names = {'Narendra Modi' : ['@PMOIndia','@NarendraModi'], 'Rahul Gandhi' : ['@RahulGandhi'], 'Sitaram Yechury': ['@SitaramYechury'], 'Mamata Banerjee': ['@MamataOfficial'], 'Arvind Kejriwal' : ['@ArvindKejriwal'], 'Shashi Tharoor' : ['@ShashiTharoor'], 'Devendra Fadnavis' : ['@Dev_Fadnavis'], 'Amit Shah' : ['@AmitShah'], 'Priyanka Gandhi' : ['@PriyankaGandhi'], 'Chandrababu Naidu' : ['@ncbn'], 'Mayawati' : ['@Mayawati'], 'Nitish Kumar': ['@NitishKumar'], 'Sushma Swaraj' : ['@SushmaSwaraj'], 'Smriti Irani' : ['@SmritiIrani'], 'Yogi Adityanath' : ['@MYogiAdityanath']}

names_and_sentiments = {}

for name in names.keys():
    for handle in names[name]:
#es.search(index="tweets", body={"size":2000,"query": {"match_all": {}},"sort":{"id":   { "order": "asc" }}})
        res = es.search(index="tweets", body={"size" : 10000,
  "query": {
    "bool": {
          "minimum_should_match": 1,
          "should": [
            {
              "regexp": {
                "tweet": ".*" + handle + ".*"
              }
            },
            {
              "regexp": {
                "tweet":  ".*" + handle.upper() + ".*"
              }
            },
            {
              "regexp": {
                "tweet": ".*" + handle.lower() + ".*"
              }
            }
          ]
    }
  }
})
    tweets = [n['_source']['tweet'] for n in res['hits']['hits']]
    
    sentiments = []

    for tweet in tweets:
        blob = TextBlob(tweet)
        sentiments.append(blob.sentences[0].sentiment.polarity)

    names_and_sentiments[name] = {'length' : len(res['hits']['hits']),'average_sentiment' : np.mean(np.asarray(sentiments))}

print(names_and_sentiments)

rc = redis_cache()

rc.set_redis(names_and_sentiments, 'names_and_sentiments')
