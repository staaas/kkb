from datetime import datetime, timedelta

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.utils.dateformat import format as django_date
from django.contrib.markup.templatetags.markup import markdown

from models import CinemaClubEvent


FUTURE_DAYS_TO_DISPLAY = 5
NUMBER_OF_ITEMS_TO_DISPLAY = 15

class CalendarRss(Feed):
    title = _(u'kina.klub.by / calendar')
    link = "/calendar/"
    description = _(u"Upcoming cinemaclub events")

    def items(self):
        now = datetime.now()
        future_day = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + \
            timedelta(days=FUTURE_DAYS_TO_DISPLAY)
        qs = CinemaClubEvent.objects.filter(
            published=True, starts_at__lte=future_day).order_by('-starts_at')
        return qs[:NUMBER_OF_ITEMS_TO_DISPLAY]

    def item_title(self, item):
        return '%s | %s' % (django_date(item.starts_at, "j E (l), G:i"),
                           item.get_short_post())

    def item_description(self, item):
        return markdown(item.description)

calendar = CalendarRss()
