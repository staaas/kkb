from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

if settings.DEBUG:
    urlpatterns = patterns('', (r'^site_media/media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),)
    urlpatterns += patterns('', (r'^site_media/static/(?P<path>.*)$',
                                 'django.views.static.serve',
                                 {'document_root': settings.STATIC_ROOT}),)
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

    url(r'^event/add/',
        'cinemaclubs.views.cinemaclubevent_add',
        name='cinemaclubevent_add'),
    url(r'^event/(?P<event_id>\d+)/edit_poster/',
        'cinemaclubs.views.cinemaclubevent_edit_poster',
        name='cinemaclubevent_edit_poster'),
    url(r'^event/(?P<event_id>\d+)/crop_poster/(?P<tmp_img_id>\d+)/',
        'cinemaclubs.views.cinemaclubevent_crop_poster',
        name='cinemaclubevent_crop_poster'),

    url(r'^event/(?P<event_id>\d+)/', 'cinemaclubs.views.someevent',
        name='someevent'),
    url(r'^(?P<cinemaclub_slug>\w+)/(?P<event_id>\d+)/',
        'cinemaclubs.views.cinemaclubevent', name='cinemaclubevent'),

    url(r'^(?P<cinemaclub_slug>\w+)/$', 'cinemaclubs.views.cinemaclub_about',
        name='cinemaclub_about'),

)
