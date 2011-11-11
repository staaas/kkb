import tweepy

from django.conf import settings


class TwitterStatus(object):
    '''
    Pyres class for submitting status to Twitter.
    '''
    queue = settings.PYRES_DEFAULT_QUEUE

    @staticmethod
    def perform(text):
        '''
        Delayed task.
        '''
        auth = tweepy.OAuthHandler(settings.PUBLISHING_TWITTER_CONSUMER_KEY,
                                   settings.PUBLISHING_TWITTER_CONSUMER_SECRET,
                                   secure=True)
        auth.set_access_token(settings.PUBLISHING_TWITTER_ACCESS_KEY,
                              settings.PUBLISHING_TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(text)
