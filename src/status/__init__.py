from pyres import ResQ

from .twitter import TwitterStatus
from .facebookuser import FacebookStatus
from .vkontakte import VkontakteStatus
from .livejournal import LivejournalPost

def publish(text, url=None):
    '''
    Publish status to social networks.
    '''
    r = ResQ()
    r.enqueue(TwitterStatus, text, url)
    r.enqueue(FacebookStatus, text, url)
    r.enqueue(VkontakteStatus, text, url)

def lj_publish(subject, text):
    '''
    Publish cumulative post to Livejournal.
    '''
    r = ResQ()
    r.enqueue(LivejournalPost, subject, text)
    
