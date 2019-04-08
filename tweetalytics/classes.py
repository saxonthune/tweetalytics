import statistics
import twitter

class feed_timeline:
    """Container for list of user tweets"""

    def __init__(self, api):
        self.timeline = []
        #todo: set timeline with user's own id

    def set_timeline(self, api, user_id):
        """Returns list of user's last 24 hours
        of tweets, or their most recent 3200 tweets, 
        depending on which is smaller."""

class feed_user:
    """container for twitter user (see api) and
    statistics for user's tweet in 24 hour window"""

    def __init__(self, user):
        self.user = user
        self.count = 0
        self.spammer = False


class feed_user_coll:
    """a list of feed_user objects and related
    methods to generate necessary statistics"""

    def __init__(self):
        self.followed_users = {}
        self.followed_users_list = []
        self.statuses_total = 0

    def add_user(self, user):
        self.followed_users[user.id] = user

    def set_statuses_total(self):
        """Tally all tweets in interval; used to
        flag spammers"""
        self.statuses_total = 0
        for u in self.followed_users:
            self.statuses_total += u.status_count

    def parse_timeline(self, feed_timeline):
        """Iterates over feed_timeline object, adds users to list,
        tallies total tweets and tweets for each user"""
        #todo

    def get_sorted_list(self):
        """Creates sorted list of users by tweet count"""
        #todo

    def flag_spammers(self): 
        """Marks users in 10th decile for tweet
        volume as spammers"""
        statuses_tally = 0
        idx = 0
        while statuses_tally < self.statuses_total / 10:
            self.followed_users_list[idx].spammer = True
            statuses_tally += self.followed_users_list[idx].count
            idx += 1


class feed_hour:
    """container for stats about tweets in
    an hour interval"""

    def __init__(self):
        self.start = None #todo: timestamp
        self.status_count = 0
        self.spam_count = 0

class feed_hour_list:
    """a list of feed_hour objects and related
    methods to generate time-based tweet
    statistics"""

    def __init__(self):
        self.hour_list = []
        self.stats = {}

    def set_hour_list(self):
        """creates list of feed_hour objects; the first
        item represents the most recent full hour (e.g.,
        at 15:20GMT, the first hour will cover 14:00-14:59GMT),
        and each sequential entry represents the preceding hour"""

    
    def parse_timeline(self, feed_timeline, feed_user_coll):
        """parses a feed_timeline to fill feed_hour objects with
        tweet tallies; if a feed_user_coll is provided, tweets from
        spammers will also be tallied"""

    def set_stats(self):
        """fetches summary statistics (maximum, minimum, median, mean)
        from a feed_hour list"""
        #todo: check if hour list has data
        self.stats['max'] = self.set_max()
        self.stats['min'] = self.set_min()
        self.stats['median'] = self.set_median()
        self.stats['mean'] = self.set_mean()

    def set_max(self):
        return max(self.hour_list, key=lambda h: h.status_count)
    def set_min(self):
        return min(self.hour_list, key=lambda h: h.status_count)

    def set_median(self):
        temp_count_list = []
        for h in self.hour_list:
            temp_count_list.append(h.count)
        return statistics.median(temp_count_list)

    def set_mean(self):
        temp_count_list = []
        for h in self.hour_list:
            temp_count_list.append(h.count)
        return statistics.mean(temp_count_list)