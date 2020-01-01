import twitter 
from datetime import datetime

def get_tweets_interval(api, start_time, end_time):
	# impelement me
	return None

def trim_tweets_to_interval(tweets, start_time, end_time):

	if len(tweets) == 0:
		return tweets

	pos = len(tweets)-1
	oldest_timestamp = datetime.strptime(tweets[pos].created_at, '%a %b %d %H:%M:%S %z %Y')

	while end_time > oldest_timestamp:

		pos -= 1
		if pos < 0:
			print('\tNo tweets in interval')
			return []
		try:
			oldest_timestamp = datetime.strptime(tweets[pos].created_at, '%a %b %d %H:%M:%S %z %Y')
		except:
			print('pos is',pos)
			return tweets
		# todo: binary search for oldest tweet

	tweets = tweets[:pos+1]
	print('\tFound',len(tweets),'tweets')
	return tweets