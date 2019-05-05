import os

from flask import Flask, Response
from flask import render_template, redirect

import json

from redis_script import *


app = Flask(__name__)

r = redis_cache()


top_topics = r.get_redis('top_topics')
names_and_sentiments = r.get_redis('names_and_sentiments')
headlines = r.get_redis('headlines')

with open('Politicians.json') as json_file:  
    people_details = json.load(json_file)

for name, dets in names_and_sentiments.items():
	for p_name in people_details['politicians']:
		if p_name['name']==name:
			names_and_sentiments[name].update({'affiliation':p_name['affiliation'], 'state': p_name['state']})
			print(names_and_sentiments[name])


total_docs = 0
news_headlines = {'headline1', 'headline2'}
for k,v in top_topics.items():
	total_docs += v['length']

@app.route("/")
def template_test():
    return render_template('index.html', topics=top_topics, topic_docs=total_docs, headlines=headlines, politicians=names_and_sentiments)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
