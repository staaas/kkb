from pyres import ResQ

from .twitter import TwitterStatus
from .facebookuser import FacebookStatus

def publish(text):
    '''
    Publish status to social networks.
    '''
    r = ResQ()
    r.enqueue(TwitterStatus, text)
    r.enqueue(FacebookStatus, text)
