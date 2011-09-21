from django.contrib import admin
from django.utils.translation import ugettext as _

from models import BlogEntry


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'author', 'published_at', 'published']
    list_filter = ['author', 'published']

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'description', 'text',)}),
        (_('Publishing'), {'fields': ('published', 'published_at', 'author')}),
    )

    actions = ['action_publish', 'action_unpublish']
    actions_selection_counter = False

    def action_publish(self, request, queryset):
        queryset.update(published=True)
    action_publish.short_description = _(u'Publish')

    def action_unpublish(self, request, queryset):
        queryset.update(published=False)
    action_unpublish.short_description = _(u'Unpublish')

admin.site.register(BlogEntry, BlogEntryAdmin)


