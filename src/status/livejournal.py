import xmlrpclib
from datetime import datetime

from django.conf import settings
from pyres import ResQ


# ref: http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.postevent.html
LJ_XML_RPC = 'http://www.livejournal.com/interface/xmlrpc'

class LivejournalPost(object):
    '''
    Pyres class for submitting status to Livejournal.
    '''
    queue = settings.PYRES_DEFAULT_QUEUE

    @staticmethod
    def perform(target, subj, text):
        username, pwd_hash, extra_params = settings.PUBLISHING_LJ_TARGETS[target]

        server = xmlrpclib.ServerProxy(LJ_XML_RPC)
        now = datetime.now()

        args = {"username" : username,
                "hpassword" : pwd_hash,
                "event" : text.encode('utf-8'),
                "subject" : subj.encode('utf-8'),
                "year" : now.year,
                "mon" : now.month,
                "day" : now.day,
                "hour": now.hour,
                "min" : now.minute
                }
        args.update(extra_params)

        server.LJ.XMLRPC.postevent(args)

def publish(subject, text):
    '''
    Publish cumulative post to Livejournal.
    '''
    r = ResQ()
    for target in settings.PUBLISHING_LJ_TARGETS.iterkeys():
        r.enqueue(LivejournalPost, target, subject, text)
