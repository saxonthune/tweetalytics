import twitter
from . import feed_helper
from datetime import datetime

class feed_user:
	"""container for twitter user (see api) and
	statistics for user's tweet in 24 hour window"""

	def __init__(self, user):
		self.user = user
		self.spammer = False
		self.tweets = []

	def add_tweet(self, tweet):
		self.tweets.append(tweet)

	def get_tweets(self, api, time_start, time_end):
		
		try:
			tweets_in_interval = api.GetUserTimeline(user_id=self.user.id, count=200, trim_user=True)
		except:
			print('Error')
			return []

		if len(tweets_in_interval) == 0:
			return []
		earliest_tweet = min(tweets_in_interval, key=lambda x: x.id)
		earliest_datetime = datetime.strptime(earliest_tweet.created_at, '%a %b %d %H:%M:%S %z %Y')

		if (earliest_datetime < time_end):
			tweets_in_interval = feed_helper.trim_tweets_to_interval(
					tweets_in_interval, time_start, time_end)
			self.tweets.extend(tweets_in_interval)
			return

		while True:
			tweets = api.GetUserTimeline(user_id=self.user.id, count=200, 
					max_id=earliest_tweet.id, trim_user=True)
			new_earliest_tweet = min(tweets, key=lambda x: x.id)
			new_earliest_datetime = datetime.strptime(earliest_tweet.created_at, 
					'%a %b %d %H:%M:%S %z %Y')

			if (	not tweets
					or earliest_tweet.id == new_earliest_tweet.id
					or new_earliest_datetime.created_at < time_end):
				break
			else:
				earliest_tweet = new_earliest_tweet
				tweets_in_interval += tweets

		tweets_in_interval = feed_helper.trim_tweets_to_interval(
				tweets_in_interval, time_start, time_end)
		print('total length:',len(tweets_in_interval))
		self.tweets.extend(tweets_in_interval)
		return