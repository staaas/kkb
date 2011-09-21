from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class BlogEntry(models.Model):
    id = models.AutoField(primary_key = True)
    slug = models.SlugField(max_length=40, default='',
                                verbose_name=_(u'Slug'))
    published = models.BooleanField(null=False, default=True,
                                verbose_name=_(u'Published'))
    published_at = models.DateTimeField(default=datetime.now,
                                        verbose_name=_(u'Published at'))
    author = models.ForeignKey(User, null=True, default=None,
                                verbose_name=_(u'Author'))

    # to be translated
    title = models.CharField(max_length=150, default='',
                                verbose_name=_(u'Title'))
    description = models.TextField(default='',
                                   verbose_name=_(u'Description'))
    text = models.TextField(default='',
                            verbose_name=_(u'Text'))


