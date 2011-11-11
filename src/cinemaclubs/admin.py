from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.conf.urls.defaults import patterns, url
from django.shortcuts import redirect
from django.forms.formsets import formset_factory
from pyres import ResQ

from commonutils.decorators import render_to
from models import CinemaClub, CinemaClubEvent, SocialPoster,\
    SOCIAL_POSTER_STATUSES_DICT, SOCIAL_SERVICES_DICT
from forms import SeparateMessagingServicesForm
from publishing import Twitter

class CinemaClubAdmin(admin.ModelAdmin):
    pass
admin.site.register(CinemaClub, CinemaClubAdmin)

SOCIAL_NETWORKS_SEND_EVENTS_LIMIT = 20

class CinemaClubEventChangeList(ChangeList):
    def get_results(self, request):
        super(CinemaClubEventChangeList, self).get_results(request)
        social_posters = SocialPoster.objects.filter(event__in=self.result_list)
        event_soc_posters = {}
        for pstr in social_posters:
            event_soc_posters.setdefault(pstr.event_id, []).append(pstr)
        for event in self.result_list:
            event.social_posters = event_soc_posters.get(event.id, [])

class CinemaClubEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'organizer', 'starts_at', 'published',
                    'display_social_posters']
    list_filter = ['organizer']

    fieldsets = (
        (None, {'fields': ('name', 'organizer', 'short_description',
                           'description', 'published')}),
        (_('Scheduling'), {'fields': ('starts_at', 'ends_at')}),
        (_('Images'), {'fields': ('poster',)}),
    )

    actions = ['action_publish', 'action_unpublish', 'action_social_networks']
    actions_selection_counter = False

    def get_changelist(self, request):
        return CinemaClubEventChangeList

    def display_social_posters(self, obj):
        return ', '.join(
            '%s (%s)' % (SOCIAL_SERVICES_DICT[p.service],
                         SOCIAL_POSTER_STATUSES_DICT[p.status]) \
                for p in obj.social_posters)
    display_social_posters.short_description = _('Social networks')

    def action_publish(self, request, queryset):
        queryset.update(published=True)
    action_publish.short_description = _(u'Publish')

    def action_unpublish(self, request, queryset):
        queryset.update(published=False)
    action_unpublish.short_description = _(u'Unpublish')

    def action_social_networks(self, request, queryset):
        if queryset.count() > SOCIAL_NETWORKS_SEND_EVENTS_LIMIT:
            messages.error(request,
                           _('You shouldn\'t normally publish more '\
                                 'than %s events to social networks') % \
                               SOCIAL_NETWORKS_SEND_EVENTS_LIMIT)
            return
        event_ids = (str(e[0]) for e in queryset.values_list('id'))
        messages.error(request, '111')
        return redirect('send/%s/' % ','.join(event_ids))
    action_social_networks.short_description = _(u'Send to social networks')

    def get_urls(self):
        urls = super(CinemaClubEventAdmin, self).get_urls()
        custom_urls = patterns('',
            url(r'^send/(?P<event_ids>(\d+,)*\d+)/$',
                self.send_to_social_networks,
                name='send_to_social_networks')
        )
        return custom_urls + urls

    @staticmethod
    @render_to('admin/cinemaclubs/send_to_social_networks.html')
    def send_to_social_networks(request, event_ids):
        event_ids = [int(eid) for eid in event_ids.split(',')]
        events = sorted(CinemaClubEvent.objects.filter(id__in=event_ids),
                        key=lambda event: event.starts_at)
        SeparateServicesFormset = formset_factory(
            SeparateMessagingServicesForm, extra=0)
        formset = SeparateServicesFormset(
            request.POST or None,
            initial=[dict(event=str(e.id), twitter=e.get_short_post()) for \
                         e in events])
        if request.method == 'POST' and formset.is_valid():
            for form in formset:
                event_id = int(form.cleaned_data['event'])
                text = form.cleaned_data['twitter']
                ResQ().enqueue(Twitter, event_id, text)
        return {'formset': formset}

admin.site.register(CinemaClubEvent, CinemaClubEventAdmin)

