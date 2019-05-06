import os

from flask import Flask, Response
from flask import render_template, redirect

import json

app = Flask(__name__)

# **************************** Comment for local ********************************************* #

from redis_script import *

r = redis_cache()

top_topics = r.get_redis('top_topics')
names_and_sentiments = r.get_redis('names_and_sentiments')
headlines = r.get_redis('headlines')
# **************************** ------------------- ********************************************* #

# **************************** Uncomment for local ********************************************* #
# top_topics = {'bjp':{'length':33, 'average_sentiment': 0.5}, 'blsfkjp':{'length':33, 'average_sentiment': 0.5}, 'bfldjp':{'length':33, 'average_sentiment': 0.5}, 'bjpew':{'length':33, 'average_sentiment': 0.5}, 'bjpuhg':{'length':33, 'average_sentiment': 0.5}, 'bjpuigfdxz':{'length':33, 'average_sentiment': 0.5}}
# names_and_sentiments = {'Narendra Modi': {'length': 537, 'average_sentiment': -0.08406999967754157}, 'Rahul Gandhi': {'length': 251, 'average_sentiment': 0.04989680527529133}, 'Sitaram Yechury': {'length': 6, 'average_sentiment': 0.005555555555555559}, 'Mamata Banerjee': {'length': 10, 'average_sentiment': -0.01499999999999999}, 'Arvind Kejriwal': {'length': 481, 'average_sentiment': 0.06902139498293346}, 'Shashi Tharoor': {'length': 4, 'average_sentiment': 0.1375}, 'Devendra Fadnavis': {'length': 2, 'average_sentiment': 0.0}, 'Amit Shah': {'length': 68, 'average_sentiment': 0.08778966131907309}, 'Priyanka Gandhi': {'length': 62, 'average_sentiment': 0.04803556658395368}, 'Chandrababu Naidu': {'length': 11, 'average_sentiment': 0.002272727272727272}, 'Mayawati': {'length': 24, 'average_sentiment': -0.004811507936507932}, 'Nitish Kumar': {'length': 2, 'average_sentiment': 0.75}, 'Sushma Swaraj': {'length': 2, 'average_sentiment': -0.0625}, 'Smriti Irani': {'length': 27, 'average_sentiment': 0.0018518518518518576}, 'Yogi Adityanath': {'length': 11, 'average_sentiment': 0.07581660763478947}}
# headlines = {'0': '"Your Father\'s Life Ended As \'Corrupt No. 1\'": PM Modi To Rahul Gandhi', '1': 'No poll code violation: PM Modi gets EC’s sixth clean chit for ‘qatal ki raat’ speech', '2': 'Eurovision rehearsals begin amid escalation', '3': 'Nobody Knows Who Runs Pakistan & Should Be Engaged For Talks, Says PM Modi', '4': 'After first two split calls, EC gives PM Modi 4th unanimous nod'}
# **************************** ------------------- ********************************************* #
 
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
