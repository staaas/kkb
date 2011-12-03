import facebook

from django.conf import settings
from pyres import ResQ


class FacebookLink(object):
    '''
    Pyres class for submitting status to Facebook.
    '''
    queue = settings.PYRES_DEFAULT_QUEUE

    @staticmethod
    def get_token(use_page):
        if not use_page:
            return "me", settings.PUBLISHING_FACEBOOK_ACCESS_TOKEN

        graph = facebook.GraphAPI(settings.PUBLISHING_FACEBOOK_ACCESS_TOKEN)
        resp = graph.get_object("me/accounts")
        if 'data' not in resp:
            raise ValueError('Response for "me/accounts" doesn\'t contain '\
                                 'data: %s' % resp)

        for account in resp['data']:
            if account['id'] == settings.PUBLISHING_FACEBOOK_PAGE_ID:
                return account['id'], account['access_token']

        raise ValueError('Failed to find page %s in "me/accounts": %s' %\
                             (settings.PUBLISHING_FACEBOOK_PAGE_ID, resp))


    @staticmethod
    def perform(text, link, image, use_page):
        '''
        Delayed task.
        '''
        fb_obj, token = FacebookLink.get_token(use_page)

        kwargs = {'message': text}
        kwargs['link'] = link
        kwargs['picture'] = image

        for key, value in kwargs.items():
           if isinstance(value, unicode):
               kwargs[key] = value.encode('utf-8')

        graph = facebook.GraphAPI(token)
        graph.put_object(fb_obj, "links", **kwargs)

def publish(text, link, image):
    r = ResQ()
    r.enqueue(FacebookLink, text, link, image, True)
    r.enqueue(FacebookLink, text, link, image, False)
