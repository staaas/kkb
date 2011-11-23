from datetime import datetime, timedelta

import redis
from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand
from django.utils.dateformat import format as django_date
from django.utils import translation
from django.conf import settings

from cinemaclubs.models import CinemaClubEvent
import status

REDIS_KEY = 'socstatus:%s'
REDIS_EXPIRE = 60 * 60 * 24 * 30  # 30 days in seconds

class Command(BaseCommand):
    help = 'Submit tomorrow events to social networks'

    def handle(self, *args, **options):
        translation.activate('be')

        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        CommandWorker(today, _(u'Today'), self.stdout).publish()
        CommandWorker(tomorrow, _(u'Tomorrow'), self.stdout).publish()

class CommandWorker(object):
    def __init__(self, date, date_text, stdout):
        self.date = date
        self.date_text = date_text
        self.stdout = stdout

    def get_status_text(self, event):
        return '%s! %s' % (self.date_text, event.get_short_post())

    def filter_new(self, events):
        r = redis.Redis()
        result = []

        key = REDIS_KEY % self.date.strftime('%Y%m%d')
        if r.exists(key):
            expire = False
        else:
            expire = True

        for event in events:
            if not r.sismember(key, event.id):
                result.append(event)
                r.sadd(key, event.id)

        if expire:
            r.expire(key, REDIS_EXPIRE)

        return result

    def get_events(self):
        date_start = datetime(year=self.date.year, month=self.date.month,
                                  day=self.date.day, hour = 0, minute=0,
                                  second=0)
        date_end = datetime(year=self.date.year, month=self.date.month,
                                day=self.date.day, hour = 23, minute=59,
                                second=59)

        date_events = CinemaClubEvent.objects.filter(
            published=True,
            starts_at__gte=date_start,
            starts_at__lte=date_end).order_by('starts_at')

        return self.filter_new(date_events)

    def publish(self):
        date_events = self.get_events()

        for event in date_events:
            text = self.get_status_text(event)
            url = event.get_short_url()
            self.stdout.write('Publishing:\n%s\n\n' % text)
            status.publish(text, url)

        if date_events:
            lj_subject = u'%s :: %s' % (django_date(self.date, "l, j E"),
                                        settings.SITE_NAME)
            lj_html = '<br />'.join(e.get_html_post() for e in date_events)
            status.lj_publish(lj_subject, lj_html)
