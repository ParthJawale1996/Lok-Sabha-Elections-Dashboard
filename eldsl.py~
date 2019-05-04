from elasticsearch import Elasticsearch
import nltk
from elasticsearch_dsl import Search
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as mplt
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from wordcloud import WordCloud
from redis_script import *

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

es = Elasticsearch()

res = es.search(index="tweets", body={"size":2000,"query": {"match_all": {}},"sort":{"id":   { "order": "asc" }}})

tweets = []
ids = []
for i in range(0,2000):
    tweets.append(res['hits']['hits'][i]['_source']['tweet'])
    ids.append(res['hits']['hits'][i]['_source']['id'])

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in tweets]   

dictionary = corpora.Dictionary(doc_clean)

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

Lda = gensim.models.ldamodel.LdaModel

ldamodel = Lda(doc_term_matrix, num_topics=7, id2word = dictionary, passes=50)

topic_list = ldamodel.show_topics(7)
get_document_topics = [ldamodel.get_document_topics(item) for item in doc_term_matrix]

topic_dict = {}

for el in topic_list:
    topic_dict[el[0]] = el[1].split('"')[3]

topic_per_document = []

for scores in get_document_topics:
    sorted_scores = sorted(scores, key=lambda x: (x[1]), reverse=True)
    topic_per_document.append(sorted_scores[0][0])

topic_sentiment_dict = {}

for i,s in enumerate(tweets):
    blob = TextBlob(s)
    for sentence in blob.sentences:
        if topic_dict[topic_per_document[i]] not in topic_sentiment_dict:
            topic_sentiment_dict[topic_dict[topic_per_document[i]]] = [sentence.sentiment.polarity]
        else:
            topic_sentiment_dict[topic_dict[topic_per_document[i]]].append(sentence.sentiment.polarity)

topic_sentiment_avgdict = {}
for k,v in topic_sentiment_dict.items():
        # v is the list of grades for student k
    topic_sentiment_avgdict.update({k: {'average_sentiment' : sum(v)/ float(len(v)),'length' : len(v)}})

print(topic_sentiment_avgdict)

rc = redis_cache()

rc.set_redis(topic_sentiment_avgdict, 'top_topics')

bjp_tweets = []

non_bjp_tweets = []

bad_list = ['rt','https','truncated','status','user','geo','text','contributors','name','replies','co']

for tweet in tweets:
    tokenized_tweet = nltk.word_tokenize(tweet.lower())
    tw = " ".join([t for t in tokenized_tweet if t not in bad_list])
    if 'bjp' in tokenized_tweet:
        bjp_tweets.append(tw)
    else:
        non_bjp_tweets.append(tw)

bjp_wordcloud = WordCloud(width=1600, height=800, max_font_size=200).generate(str(bjp_tweets))
mplt.figure(figsize=(12, 10))
mplt.imshow(bjp_wordcloud, interpolation="bilinear")
mplt.axis("off")
mplt.savefig('bjp_wordcloud.png')

non_bjp_wordcloud = WordCloud(width=1600, height=800, max_font_size=200).generate(str(non_bjp_tweets))
mplt.figure(figsize=(12, 10))
mplt.imshow(non_bjp_wordcloud, interpolation="bilinear")
mplt.axis("off")
mplt.savefig('non_bjp_wordcloud.png')



