import os

from flask import Flask, Response
from flask import render_template, redirect

from redis_script import *


app = Flask(__name__)

r = redis_cache()


top_topics = r.get_redis('top_topics')

print(top_topics)
total_docs = 0
news_headlines = {'headline1', 'headline2'}
for k,v in top_topics.items():
	total_docs += v['length']

@app.route("/")
def template_test():
    return render_template('index.html', topics=top_topics, topic_docs=total_docs, headlines=list(news_headlines))


if __name__ == '__main__':
    app.run(debug=True)