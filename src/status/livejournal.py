import xmlrpclib
from datetime import datetime

from django.conf import settings


# ref: http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.postevent.html
LJ_XML_RPC = 'http://www.livejournal.com/interface/xmlrpc'

class LivejournalPost(object):
    '''
    Pyres class for submitting status to Livejournal.
    '''
    queue = settings.PYRES_DEFAULT_QUEUE

    @staticmethod
    def perform(subj, text):
        server = xmlrpclib.ServerProxy(LJ_XML_RPC)
        now = datetime.now()

        args = {"username" : settings.PUBLISHING_LJ_UNAME,
                "hpassword" : settings.PUBLISHING_LJ_PWD,
                "event" : text.encode('utf-8'),
                "subject" : subj,
                "year" : now.year,
                "mon" : now.month,
                "day" : now.day,
                "hour": now.hour,
                "min" : now.minute
                }
        # call the remote method as a method of the server object
        server.LJ.XMLRPC.postevent(args)

LJ_TEMPLATE = \
    '<a href="%(evurl)s"><img width="150px" height="150px"'\
    'style="border: 0; display: inline; float: right;" src="%(evimg)s" /></a>'\
    '<h4><a href="%(evurl)s">%(evtitle)s</a></h4>'\
    '<p>%(evdesc)s <a href="%(evurl)s">(%(readmore)s)</a></p>'\
    '<p>%(org)s: <a href="%(ccurl)s">%(ccname)s</a></p>'\
    '<p>%(starts)s: %(evstarts)s</p><div style="clear: both"></div>'

def format_event(e):
    return LJ_TEMPLATE % {
        'evurl': e.get_absolute_url(),
        'evimg': e.poster_span3.url,
        'evtitle': e.name,
        'evdesc': e.short_description,
        'readmore': 'Read more',
        'org': 'Organizer',
        'ccurl': e.organizer.get_absolute_url(),
        'ccname': e.organizer,
        'starts': 'Starts at',
        'evstarts': e.starts_at.strftime('%m.%s %H:%M')}
