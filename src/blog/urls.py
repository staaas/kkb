from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        'post_detail', name="blog_post_detail"),
    url(r'^$', 'posts', name='blog_posts'),
)
