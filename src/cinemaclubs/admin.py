from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.conf.urls.defaults import patterns, url
from django.shortcuts import redirect
from django.forms.formsets import formset_factory
from pyres import ResQ

from commonutils.decorators import render_to
from models import CinemaClub, CinemaClubEvent
from forms import SeparateMessagingServicesForm

class CinemaClubAdmin(admin.ModelAdmin):
    pass
admin.site.register(CinemaClub, CinemaClubAdmin)

SOCIAL_NETWORKS_SEND_EVENTS_LIMIT = 20

class CinemaClubEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'organizer', 'starts_at', 'published']
    list_filter = ['organizer']

    fieldsets = (
        (None, {'fields': ('name', 'organizer', 'short_description',
                           'description', 'published')}),
        (_('Scheduling'), {'fields': ('starts_at', 'ends_at')}),
        (_('Images'), {'fields': ('poster',)}),
    )

    actions = ['action_publish', 'action_unpublish']
    actions_selection_counter = False

    def action_publish(self, request, queryset):
        queryset.update(published=True)
    action_publish.short_description = _(u'Publish')

    def action_unpublish(self, request, queryset):
        queryset.update(published=False)
    action_unpublish.short_description = _(u'Unpublish')

admin.site.register(CinemaClubEvent, CinemaClubEventAdmin)

