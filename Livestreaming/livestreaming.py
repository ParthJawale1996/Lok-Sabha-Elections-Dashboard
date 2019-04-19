import tweepy
import codecs
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from cassandra.cluster import Cluster


class LiveStreaming:


	def __init__(self,key_store,hashtag):

		self.key_store = key_store
		self.hashtag = hashtag


		self.consumer_key,self.consumer_secret,self.access_token,self.access_secret = self.read_keys(self.key_store)


		self.api = self.api_authenticate()

		self.tweet_writer()
		





	def read_keys(self,filename):


		with open(filename) as f:
			keys = f.readlines()
			keys = [x.strip() for x in keys]
			return (keys[0],keys[1],keys[2],keys[3])



	def api_authenticate(self):

		auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_secret)

		api = tweepy.API(auth)

		return api



	def tweet_writer(self):

		#hashtag = input("Enter #tag here")
		f = codecs.open('tweet.txt','w',encoding='utf-8')

		cluster = Cluster()
		session = cluster.connect()
		
		for tweet in tweepy.Cursor(self.api.search,q=self.hashtag,count=100,lang="en",since_id=2016-10-11).items():
			print (tweet.created_at, tweet.text)
			preparedTweetInsert = session.prepare(
			"""
			INSERT INTO tweets.tweet_table (tweet)
			VALUES (?)
			""")
			session.execute(preparedTweetInsert,[tweet.created_at,tweet.text])
			f.write("%s,%s\ufeff" %(tweet.created_at, tweet.text))
		f.close()
		




if __name__ == '__main__':

	h = '#hero'
	livestream = LiveStreaming('keys.txt',h)






	
	



