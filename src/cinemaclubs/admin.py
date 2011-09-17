from django.contrib import admin
from django.utils.translation import ugettext as _

from models import CinemaClub, CinemaClubEvent

class CinemaClubAdmin(admin.ModelAdmin):
    pass
admin.site.register(CinemaClub, CinemaClubAdmin)

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

    #date_hierarchy = 'starts_at'

    def action_publish(self, request, queryset):
        queryset.update(published=True)
    action_publish.short_description = _(u'Publish')

    def action_unpublish(self, request, queryset):
        queryset.update(published=False)
    action_unpublish.short_description = _(u'Unpublish')

admin.site.register(CinemaClubEvent, CinemaClubEventAdmin)

