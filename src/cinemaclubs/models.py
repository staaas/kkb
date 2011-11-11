from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils import dateformat
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

    slug = models.SlugField(max_length=40, default='')

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

class CinemaClubEvent(ImageModel):
    id = models.AutoField(primary_key = True)
    organizer = models.ForeignKey('CinemaClub')
#    geo_coordinates = models.CharField(max_length=50)
    starts_at = models.DateTimeField(null=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    poster = models.ImageField(null=True, upload_to=UPLOAD_DIR)
    published = models.BooleanField(null=False, default=False)

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
        text = '%(organizer)s - %(title)s %(url)s' % {
            'organizer': self.organizer.name_short,
            'title': self.name,
            'url': 'http://kina.klu.by%s' % self.get_short_url()}
        return text[:140]

TMP_UPLOAD_DIR = 'tmpimg'

class TemporaryImage(ImageModel):
    image = models.ImageField(null=True, upload_to=TMP_UPLOAD_DIR)
    created = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, default=None)

    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)

SOCIAL_SERVICE_TWITTER = 0
SOCIAL_SERVICES = [(SOCIAL_SERVICE_TWITTER, 'twitter')]
SOCIAL_SERVICES_DICT = dict(SOCIAL_SERVICES)

SOCIAL_POSTER_STATUS_WAITING = 0
SOCIAL_POSTER_STATUS_SUCCESS = 1
SOCIAL_POSTER_STATUS_ERROR = 2
SOCIAL_POSTER_STATUS_EDITING = 3
SOCIAL_POSTER_STATUSES = [(SOCIAL_POSTER_STATUS_WAITING, _('Waiting')),
                          (SOCIAL_POSTER_STATUS_SUCCESS, _('Success')),
                          (SOCIAL_POSTER_STATUS_ERROR, _('Error'))]
SOCIAL_POSTER_STATUSES_DICT = dict(SOCIAL_POSTER_STATUSES)

class SocialPoster(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey('CinemaClubEvent')
    service = models.IntegerField(max_length=2, choices=SOCIAL_SERVICES,
                                  verbose_name=_(u'Service'))
    status = models.IntegerField(max_length=1, choices=SOCIAL_POSTER_STATUSES,
                                  verbose_name=_(u'Service'), default=0)
    text = models.TextField(default='')

    class Meta:
        unique_together = ("event", "service")
