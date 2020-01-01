import twitter
from datetime import datetime, timedelta
from pathlib import Path
import test_credentials as c
import sys
import json
import pickle
from collections import defaultdict

def get_tweets(api=None, screen_name=None, cutoff_time=None):
	timeline = api.GetHomeTimeline(count=200,trim_user=True)
	if len(timeline) == 0:
		print("len(timeline) is zero!")
		exit()
	earliest_tweet = min(timeline, key=lambda x: x.id).id

	while True:
		tweets = api.GetHomeTimeline(
			max_id=earliest_tweet,
			count=200,
			trim_user=True
		)
		new_earliest = min(tweets, key=lambda x: x.id).id

		if (not tweets 
				or new_earliest == earliest_tweet): 
			break
		else:
			earliest_tweet = new_earliest
			timeline += tweets

	return timeline

def create_friends(timeline=None):
	friends = defaultdict(list)
	for t in timeline:
		friends[t.user.id_str].append(t)
	return friends

if __name__ == "__main__":

	api = twitter.Api(
		c.CONSUMER_KEY,
		c.CONSUMER_SECRET,
		c.ACCESS_TOKEN_KEY,
		c.ACCESS_TOKEN_SECRET
	)
	screen_name = sys.argv[1]
	screen_name = 'zongermann'
	cutoff = datetime.now() - timedelta(days=1)
	pkl_name = './output/'+screen_name+'_timeline.pkl'

	Path('./output').mkdir(parents=True, exist_ok=True)

	try:
		timeline = get_tweets(api, screen_name, cutoff)
	except:
		print("Rate limiting detected; switching to local storage...")
		with open(pkl_name,'rb') as input:
			timeline = pickle.load(input)
	
	timeline_len = len(timeline)
	print("Oldest tweet:", timeline[ timeline_len-1 ].created_at)
	friends = create_friends(timeline)

	print("There are",timeline_len,"tweets total\n")

	csv_name = './output/'+screen_name+'_tweetsByUser.csv'
	with open(csv_name, 'w+') as file:
		file.write('user_name,count,proportion\n')
		for key in sorted(friends, key=lambda x:len(friends[x]), reverse=True):
			user_name = api.GetUser(user_id=key).screen_name
			print(
				user_name,
				len(friends[key]),
				len(friends[key])/timeline_len,
				sep='\t'
			)
			file.write(user_name)
			file.write(',')
			file.write(str(len(friends[key])))
			file.write(',')
			file.write(str(len(friends[key])/timeline_len))
			file.write('\n')

	with open(pkl_name,'wb') as file:
		pickle.dump(timeline, file, pickle.HIGHEST_PROTOCOL)
