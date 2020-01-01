import twitter
from collections import OrderedDict
from . import feed_user

class feed_user_coll:
	"""a list of feed_user objects and related
	methods to generate necessary statistics"""

	def __init__(self, user_list=None):

		self.followed_users = {}
#		self.followed_users = OrderedDict()
		self.statuses = 0
		for u in user_list:
			self.followed_users[u.id] = (feed_user.feed_user(u))

	def add_user(self, user):
		self.followed_users[user.id] = user

	def add_tweet(self, tweet):
		self.followed_users[tweet.id].add_tweet(tweet)

	def populate_all(self, api, time_start, time_end):
		for k,v in self.followed_users.items():
			print('getting tweets in interval for user:',v.user.screen_name)
			v.get_tweets(api, time_start, time_end)
		self.update_tweets_total()

	def update_tweets_total(self):
		"""Tally all tweets in interval; used to
		flag spammers"""
		self.statuses = 0
		for k,v in self.followed_users.items():
			self.statuses += len(v.tweets)
	