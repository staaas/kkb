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
                "subject" : subj.encode('utf-8'),
                "year" : now.year,
                "mon" : now.month,
                "day" : now.day,
                "hour": now.hour,
                "min" : now.minute
                }
        # call the remote method as a method of the server object
        server.LJ.XMLRPC.postevent(args)
