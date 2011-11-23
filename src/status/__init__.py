from pyres import ResQ

from .twitter import TwitterStatus
from .facebookuser import FacebookStatus
from .vkontakte import VkontakteStatus
from .livejournal import LivejournalPost, format_event as lj_format_event

def publish(text):
    '''
    Publish status to social networks.
    '''
    r = ResQ()
    r.enqueue(TwitterStatus, text)
    r.enqueue(FacebookStatus, text)
    r.enqueue(VkontakteStatus, text)

def lj_publish(subject, events):
    '''
    Publish cumulative post to Livejournal.
    '''
    text = ''.join(lj_format_event(e) for e in events)
    r = ResQ()
    r.enqueue(LivejournalPost, subject, text)
    
