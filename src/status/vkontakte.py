import urllib
import urllib2
import json
from contextlib import closing

from django.conf import settings

VK_URL = 'https://api.vkontakte.ru/method/%s?%s'

def vk(method, params):
    url = VK_URL % (method, urllib.urlencode(params))
    with closing(urllib2.urlopen(url)) as resp:
        return json.loads(resp.read())

class VkontakteStatus(object):
    '''
    Pyres class for submitting status to Vkontakte.
    '''
    queue = settings.PYRES_DEFAULT_QUEUE

    @staticmethod
    def perform(text):
        '''
        Delayed task.
        '''
        method = 'wall.post'
        params = {'owner_id': settings.PUBLISHING_VKONTAKTE_USER_ID,
                     'access_token': settings.PUBLISHING_VKONTAKTE_USER_TOKEN,
                     'message': text}
        resp = vk(method, params)
        post_id = resp.get("response", {}).get("post_id")
        if not post_id:
            raise ValueError('Post ID not provided.\nMethod %s\nParams %r\n '\
                                 'Response %r' % (method, params, resp))
