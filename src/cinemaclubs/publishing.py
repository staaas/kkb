from django.conf import settings
from cinemaclubs.models import CinemaClubEvent, SocialPoster
from cinemaclubs.models import SOCIAL_SERVICE_TWITTER
from cinemaclubs.models import SOCIAL_POSTER_STATUS_ERROR, \
    SOCIAL_POSTER_STATUS_SUCCESS, SOCIAL_POSTER_STATUS_WAITING
import tweepy
from tweepy.error import TweepError

class Twitter(object):
    service_id = SOCIAL_SERVICE_TWITTER
    queue = 'socialpub'

    @staticmethod
    def error(event, text):
        try:
            poster = SocialPoster.objects.get(event=event,
                                              service=Twitter.service_id)
        except SocialPoster.DoesNotExist:
            poster = SocialPoster(event=event,
                                  service=Twitter.service_id,
                                  text=text)
        poster.status = SOCIAL_POSTER_STATUS_ERROR
        poster.save()

    @staticmethod
    def success(event, text):
        try:
            poster = SocialPoster.objects.get(event=event,
                                              service=Twitter.service_id)
        except SocialPoster.DoesNotExist:
            poster = SocialPoster(event=event,
                                  service=Twitter.service_id,
                                  text=text)
        poster.status = SOCIAL_POSTER_STATUS_SUCCESS
        poster.save()

    @staticmethod
    def does_not_exist(event_id, text):
        pass

    @staticmethod
    def perform(event_id, text):
        try:
            event = CinemaClubEvent.objects.get(id=event_id)
        except CinemaClubEvent.DoesNotExist:
            return Twitter.does_not_exist(event_id, text)
        try:
            auth = tweepy.OAuthHandler(settings.PUBLISHING_TWITTER_CONSUMER_KEY,
                                       settings.PUBLISHING_TWITTER_CONSUMER_SECRET,
                                       secure=True)
            auth.set_access_token(settings.PUBLISHING_TWITTER_ACCESS_KEY,
                                  settings.PUBLISHING_TWITTER_ACCESS_SECRET)
            api = tweepy.API(auth)
            api.update_status(text)

            Twitter.success(event, text)
        except (TweepError,), e:
            Twitter.error(event, text)
            # log
        except:
            Twitter.error(event, text)
            raise
