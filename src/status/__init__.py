from pyres import ResQ

from .twitter import TwitterStatus
from .facebookuser import FacebookStatus
from .vkontakte import VkontakteStatus

def publish(text, url=None):
    '''
    Publish status to social networks.
    '''
    r = ResQ()
    r.enqueue(TwitterStatus, text, url)
    r.enqueue(FacebookStatus, text, url)
    r.enqueue(VkontakteStatus, text, url)
