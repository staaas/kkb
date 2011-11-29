import urllib2
import json
from contextlib import closing

from django.utils.http import urlencode
from django.conf import settings
from pyres import ResQ

VK_URL = 'https://api.vkontakte.ru/method/%s?%s'

def vk(method, params):
    url = VK_URL % (method, urlencode(params))
    with closing(urllib2.urlopen(url)) as resp:
        return json.loads(resp.read())

class VkontakteStatus(object):
    '''
    Pyres class for submitting status to Vkontakte.
    '''
    queue = settings.PYRES_DEFAULT_QUEUE

    @staticmethod
    def perform(text, url):
        '''
        Delayed task.
        '''
        if not settings.PUBLISHING_VKONTAKTE_USER:
            return
        if not url is None:
            text = '%s %s' % (text, url)

        method = 'wall.post'
        owner_id, token, extra_params = settings.PUBLISHING_VKONTAKTE_USER
        params = {'owner_id': owner_id,
                  'access_token': token,
                  'message': text}
        params.update(extra_params)
        resp = vk(method, params)
        post_id = resp.get("response", {}).get("post_id")
        if not post_id:
            raise ValueError('Post ID not provided.\nMethod %s\nParams %r'\
                                 '\n Response %r' % (method, params, resp))

        r = ResQ()
        for user, data in settings.PUBLISHING_VKONTAKTE_REPOST_USERS.iteritems():
            r.enqueue(VkontakteLike, user, owner_id, post_id)

class VkontakteLike(object):
    '''
    Pyres class for liking a post in Vkontakte.
    '''
    queue = settings.PYRES_DEFAULT_QUEUE

    @staticmethod
    def perform(user, owner_id, post_id):
        method = 'wall.addLike'
        token, extra_params = settings.PUBLISHING_VKONTAKTE_REPOST_USERS[user]
        params = {'owner_id': owner_id,
                  'access_token': token,
                  'post_id': post_id,
                  'repost': '1'}
        params.update(extra_params)
        resp = vk(method, params)
        if resp.get("response", {}).get("reposted_post_id") is None:
            raise ValueError('Failed to like a post.\nResponse %r' % resp)
