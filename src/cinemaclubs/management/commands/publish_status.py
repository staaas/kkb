from datetime import datetime, timedelta

from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand, CommandError

from cinemaclubs.models import CinemaClubEvent
import status

class Command(BaseCommand):
    help = 'Submit tomorrow events to social networks'

    def get_status_text(self, event):
        return _(u'Tomorrow! %s') % event.get_short_post()

    def handle(self, *args, **options):
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_start = datetime(year=tomorrow.year, month=tomorrow.month,
                                  day=tomorrow.day, hour = 0, minute=0,
                                  second=0)
        tomorrow_end = datetime(year=tomorrow.year, month=tomorrow.month,
                                day=tomorrow.day, hour = 23, minute=59,
                                second=59)

        tomorrow_events = CinemaClubEvent.objects.filter(
            published=True,
            starts_at__gte=tomorrow_start,
            starts_at__lte=tomorrow_end)

        for event in tomorrow_events:
            text = self.get_status_text(event)
            self.stdout.write('Publishing:\n%s\n\n' % text)
            status.publish(text)
