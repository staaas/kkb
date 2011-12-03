from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _

from models import BlogEntry


class LatestEntriesRss(Feed):
    title = _(u'KINA.KLU.BY / BLOG')
    link = "/blog/"
    description = _(u"Blog about cinema clubs and amateur '\
                    'cinema movement in Belarus")

    def items(self):
        qs = BlogEntry.objects.filter(published=True).order_by('-published_at')
        return qs[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
