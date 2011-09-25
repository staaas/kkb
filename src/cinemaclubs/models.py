from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from imagekit.models import ImageModel
from django.conf import settings


UPLOAD_DIR = 'modelimg'
IMG_MAX_SIZE = 1024
IMG_MIN_SIZE = 300

class CinemaClub(models.Model):
    id = models.AutoField(primary_key = True)
#    geo_coordinates = models.CharField(max_length=50)
    url = models.CharField(max_length=256)
    logo = models.ImageField(null=True, upload_to=UPLOAD_DIR)

    slug = models.SlugField(max_length=40, default='')

    # to be translated
    name = models.CharField(max_length=150, default='')
    mission = models.CharField(max_length=300, default='')
    description = models.TextField(default='')
    name_short = models.CharField(max_length=40, default='')  # slug for header

    curators = models.ManyToManyField(User, related_name='cinemaclubs')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cinemaclub_about', args=[self.slug,])

class CinemaClubEvent(ImageModel):
    id = models.AutoField(primary_key = True)
    organizer = models.ForeignKey('CinemaClub')
#    geo_coordinates = models.CharField(max_length=50)
    starts_at = models.DateTimeField(null=True)
    ends_at = models.DateTimeField(null=True)
    poster = models.ImageField(null=True, upload_to=UPLOAD_DIR)
    published = models.BooleanField(null=False, default=False)

    # to be translated
    name = models.CharField(max_length=150, default='')
    short_description = models.CharField(max_length=500, default='', db_column='short_desciption')
    description = models.TextField(default='')

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'cinemaclubs.ikspecs'
        cache_dir = 'eventscache'
        image_field = 'poster'
        # save_count_as = 'num_views'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.organizer:
            return reverse('cinemaclubevent', args=[self.organizer.slug,
                                                    self.id,])
        return reverse('someevent', args=[self.id,])
        

TMP_UPLOAD_DIR = 'tmpimg'

class TemporaryImage(ImageModel):
    image = models.ImageField(null=True, upload_to=TMP_UPLOAD_DIR)
    created = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, default=None)

    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)
