from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

if settings.DEBUG:
    urlpatterns = patterns('', (r'^media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),)
    urlpatterns += patterns('', (r'^static/(?P<path>.*)$',
                                 'django.views.static.serve',
                                 {'document_root': settings.MEDIA_ROOT}),)
else:
    urlpatterns = []

urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('social_auth.urls')),

    url(r'^$', 'cinemaclubs.views.home', name='home'),
    url(r'^minska/$', 'cinemaclubs.views.minsk', name='minsk'),

    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^logout/$', 'cinemaclubs.views.logout', name='logout'),

    url(r'^event/(?P<event_id>\d+)/', 'cinemaclubs.views.someevent',
        name='someevent'),
    url(r'^(?P<cinemaclub_slug>\w+)/(?P<event_id>\d+)/',
        'cinemaclubs.views.cinemaclubevent', name='cinemaclubevent'),

    url(r'^(?P<cinemaclub_slug>\w+)/$', 'cinemaclubs.views.cinemaclub_about',
        name='cinemaclub_about'),

)
