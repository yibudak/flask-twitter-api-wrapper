# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from twitter.scraper import Scraper
import logging


class TwitterWrapper:
    def __init__(self, conf, test_tweet_id=896102939026148896):
        self.conf = conf
        self.blocked = False
        self.test_tweet_id = test_tweet_id
        self.scraper = self.get_session()
        if self.check_session():
            logging.info("Session is live")

    def get_tweet(self, tweet_id):
        """
        Get tweet by id
        :param tweet_id:
        :return: dict
        """
        if not self.check_session():
            if not self.renew_session():
                raise Exception("Session is blocked")
        if self.scraper:
            try:
                data = self.scraper.tweets_by_id([tweet_id])[0]["data"]
                return data["tweetResult"]["result"]
            except Exception as e:
                logging.error(f"Error while fetching tweet: {e}")
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
                return Scraper(
                    self.conf.twitter.email,
                    self.conf.twitter.username,
                    self.conf.twitter.password,
                    debug=4,
                    save=True,
                    pbar=False,
                )
            except Exception as e:
                logging.error(f"Error while getting session: {e}")
                self.blocked = True
        return None

    def renew_session(self):
        """
        Renew the current session
        :return: bool
        """
        self.scraper = self.get_session()
        return self.scraper is not None

    def check_session(self):
        """
        Check if the current session is live
        :return: bool
        """
        if not self.blocked and self.scraper:
            try:
                self.scraper.tweet_stats([self.test_tweet_id])
                return True
            except Exception as e:
                logging.error(f"Error while checking session: {e}")
                self.scraper = None
        return False
