import os

from flask import Flask, Response
from flask import render_template, redirect


app = Flask(__name__)

top_topics = {'bjp':{'sentiment': 0.02, 'length': 320}, 'loksabha': {'sentiment': 0.42, 'length': 555}}
total_docs = 0
news_headlines = {'headline1', 'headline2'}
for k,v in top_topics.items():
	total_docs += v['length']

@app.route("/")
def template_test():
    return render_template('index.html', topics=top_topics, topic_docs=total_docs, headlines=list(news_headlines))


if __name__ == '__main__':
    app.run(debug=True)