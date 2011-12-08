from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.dateformat import format as django_date
from imagekit.models import ImageModel
from django.conf import settings


UPLOAD_DIR = 'modelimg'
IMG_MAX_SIZE = 1024
IMG_MIN_SIZE = 300

class CinemaClub(ImageModel):
    id = models.AutoField(primary_key = True)
#    geo_coordinates = models.CharField(max_length=50)
    url = models.CharField(max_length=256, null=True, blank=True)
    logo = models.ImageField(null=True, upload_to=UPLOAD_DIR)

    slug = models.SlugField(max_length=40, default='', unique=True)

    # to be translated
    name = models.CharField(max_length=150, default='')
    mission = models.CharField(max_length=300, default='')
    description = models.TextField(default='')
    name_short = models.CharField(max_length=40, default='')  # slug for header

    curators = models.ManyToManyField(User, related_name='cinemaclubs')

    class IKOptions:
        spec_module = 'cinemaclubs.imagekit_cinemaclub'
        cache_dir = 'cinemaclubscache'
        image_field = 'logo'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cinemaclub_about', args=[self.slug,])

EVENT_LJ_TEMPLATE = \
    '<a href="%(site)s%(evurl)s"><img width="150px" height="150px"'\
    'style="border: 0; display: inline; float: right;" '\
    'src="%(site)s%(evimg)s" /></a>'\
    '<h4><a href="%(site)s%(evurl)s">%(evtitle)s</a></h4>'\
    '<p>%(evdesc)s <a href="%(site)s%(evurl)s">(%(readmore)s)</a></p>'\
    '<p>%(org)s: <a href="%(site)s%(ccurl)s">%(ccname)s</a></p>'\
    '<p>%(starts)s: %(evstarts)s</p><div style="clear: both"></div>'

EVENT_TEMPLATE = \
    '%(evtitle)s\n\n'\
    '%(evdesc)s\n\n'\
    '%(org)s: %(ccname)s\n'\
    '%(starts)s: %(evstarts)s'

class CinemaClubEvent(ImageModel):
    id = models.AutoField(primary_key = True)
    organizer = models.ForeignKey('CinemaClub', db_index=True)
#    geo_coordinates = models.CharField(max_length=50)
    starts_at = models.DateTimeField(null=True, db_index=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    poster = models.ImageField(null=True, upload_to=UPLOAD_DIR)
    published = models.BooleanField(null=False, default=False, db_index=True)

    # to be translated
    name = models.CharField(max_length=150, default='')
    short_description = models.CharField(max_length=500, default='', db_column='short_desciption')
    description = models.TextField(default='')

    class IKOptions:
        spec_module = 'cinemaclubs.imagekit_event'
        cache_dir = 'eventscache'
        image_field = 'poster'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.organizer:
            return reverse('cinemaclubevent', args=[self.organizer.slug,
                                                    self.id,])
        return reverse('someevent', args=[self.id,])

    def get_short_url(self):
        if self.organizer:
            return reverse('someevent', args=[self.id,])
        return reverse('someevent', args=[self.id,])

    def get_short_post(self):
        text = '%(organizer)s - %(title)s' % {
            'organizer': self.organizer.name_short,
            'title': self.name}
        return text[:140]

    def get_post(self):
        return EVENT_TEMPLATE % {
            'evtitle': self.name,
            'evdesc': self.short_description,
            'org': _(u'Organizer'),
            'ccname': self.organizer,
            'starts': _(u'Starts at'),
            'evstarts': django_date(self.starts_at, "j E (l), G:i")}

    def get_html_post(self):
        return EVENT_LJ_TEMPLATE % {
            'evurl': self.get_absolute_url(),
            'evimg': self.poster_span3.url,
            'evtitle': self.name,
            'evdesc': self.short_description,
            'readmore': _(u'read more'),
            'org': _(u'Organizer'),
            'ccurl': self.organizer.get_absolute_url(),
            'ccname': self.organizer,
            'starts': _(u'Starts at'),
            'evstarts': django_date(self.starts_at, "j E (l), G:i"),
            'site': settings.SITE_URL,}

    def get_image_url(self):
        return self.poster_span5.url

TMP_UPLOAD_DIR = 'tmpimg'

class TemporaryImage(ImageModel):
    image = models.ImageField(null=True, upload_to=TMP_UPLOAD_DIR)
    created = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, default=None)

    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)
