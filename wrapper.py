# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from twitter.scraper import Scraper
from twitter.util import init_session


class TwitterWrapper:
    def __init__(self, conf):
        self.conf = conf
        self.blocked = False
        self.scraper = self.get_session()

    def get_tweet(self, tweet_id):
        """
        Get tweet by id
        :param tweet_id:
        :return: dict
        """
        if not self.check_session():
            self.renew_session()
        if self.scraper:
            try:
                data = self.scraper.tweets_by_id([tweet_id])[0]["data"]
                return data["tweetResult"]["result"]
            except Exception as e:
                raise e
        else:
            raise Exception("Session is blocked")

    def get_session(self):
        """
        Get a new session
        :return: Scraper object
        """
        if not self.blocked:
            try:
                session = init_session()
                return Scraper(session=session, debug=4, save=True, pbar=False)
            except Exception as e:
                self.blocked = True
        return None

    def renew_session(self):
        """
        Renew the current session
        :return: bool
        """
        self.scraper = self.get_session()
        return True

    def check_session(self):
        """
        Check if the current session is live
        :return: bool
        """
        if not self.blocked and self.scraper:
            try:
                self.scraper.tweet_stats([896102939026148896])  # @dramvemelodi
                return True
            except Exception as e:
                self.scraper = None
        return False
