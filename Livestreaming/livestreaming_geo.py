import tweepy
import codecs
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from cassandra.cluster import Cluster
from twython import Twython
import time


class LiveStreaming:


	def __init__(self,key_store,hashtag):

		self.key_store = key_store
		self.hashtag = hashtag


		self.consumer_key,self.consumer_secret,self.access_token,self.access_secret = self.read_keys(self.key_store)


		self.api = self.api_authenticate()

		#self.tweet_writer()
		self.new_tweet_writer()
		





	def read_keys(self,filename):


		with open(filename) as f:
			keys = f.readlines()
			keys = [x.strip() for x in keys]
			return (keys[0],keys[1],keys[2],keys[3])



	def api_authenticate(self):

		#auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		#auth.set_access_token(self.access_token, self.access_secret)

		#api = tweepy.API(auth)


		api = Twython(self.consumer_key,self.consumer_secret,self.access_token,self.access_secret)

		return api

	def new_tweet_writer(self):

		
		cluster = Cluster()
		session = cluster.connect()
		


		results = self.api.cursor(self.api.search, q=self.hashtag)
		#print (len(results))
		for result in results:
			#print(result['id_str'])


			
			try:
				location = result['geo']['coordinates']

					
			except (TypeError, AttributeError):


				location = None

			
			print (result['id_str'],result['text'],location)	

			preparedTweetInsert = session.prepare(
			"""
			INSERT INTO tweets.tweet_table (UUID,tweet,location)
			VALUES (?)
			""")
			session.execute(preparedTweetInsert,[result['id_str'],result['text'],location])


			time.sleep(5)

		


	def tweet_writer(self):

		#hashtag = input("Enter #tag here")
		f = codecs.open('tweet.txt','w',encoding='utf-8')

		cluster = Cluster()
		session = cluster.connect()
		
		for tweet in tweepy.Cursor(self.api.search,q=self.hashtag,count=100,lang="en",since_id=2016-10-11).items():
			print (tweet.created_at, tweet.text)
			preparedTweetInsert = session.prepare(
			"""
			INSERT INTO tweets.tweet_table (UUID,tweet)
			VALUES (?)
			""")
			session.execute(preparedTweetInsert,[tweet.created_at,tweet.text])
			f.write("%s,%s\ufeff" %(tweet.created_at, tweet.text))
		f.close()
		




if __name__ == '__main__':

	h = '#election'
	livestream = LiveStreaming('/home/cu/streaming/access_keys/keys.txt',h)