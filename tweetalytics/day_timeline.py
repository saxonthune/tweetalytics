import twitter
from models import feed_user_coll
from datetime import datetime, timedelta
from pathlib import Path
import test_credentials as c
import sys
import json
import pickle
import pytz
from collections import defaultdict


if __name__ == "__main__":

	api = twitter.Api(
		c.CONSUMER_KEY,
		c.CONSUMER_SECRET,
		c.ACCESS_TOKEN_KEY,
		c.ACCESS_TOKEN_SECRET
	)
	screen_name = sys.argv[1]
	pkl_name = './output/'+screen_name+'_24hr.pkl'
	cutoff = datetime.now() - timedelta(days=1)

	Path('./output').mkdir(parents=True, exist_ok=True)

	if (len(sys.argv) < 3):
		with open(pkl_name,'rb') as file:
			print('===INFO: Loading data from',pkl_name)
			friends_data = pickle.load(file)

	else:
		today = datetime.now(pytz.utc)
		yesterday = today - timedelta(days=1)
		friends = api.GetFriends(screen_name=screen_name)
		friends_data = feed_user_coll.feed_user_coll(friends)
		friends_data.populate_all(api, today, yesterday)
		with open(pkl_name,'wb') as file:
			print('===INFO: Saving friends list as', pkl_name)
			pickle.dump(friends_data, file, pickle.HIGHEST_PROTOCOL)

	csv_name = './output/'+screen_name+'_24hr.csv'
	with open (csv_name,'w+') as file:
		print('===INFO: saving data to',csv_name)
		file.write('screen_name,tweets,proportion\n')
		for k,v in friends_data.followed_users.items():
			file.write(v.user.screen_name)
			file.write(',')
			file.write(str(len(v.tweets)))
			file.write(',')
			file.write(str(len(v.tweets)/friends_data.statuses))
			file.write('\n')

	print('total tweets:',friends_data.statuses)