from pyres import ResQ

from .twitter import TwitterStatus
from .facebookuser import FacebookStatus
from .vkontakte import VkontakteStatus

def publish(text):
    '''
    Publish status to social networks.
    '''
    r = ResQ()
    r.enqueue(TwitterStatus, text)
    r.enqueue(FacebookStatus, text)
    r.enqueue(VkontakteStatus, text)
