from django import template

from blog.models import BlogEntry


register = template.Library()

@register.inclusion_tag('blog/tags/recent_entry.html')
def recent_blog_entry():
    try:
        recent_entry = BlogEntry.objects.filter(
            published=True).order_by('-published_at')[0]
    except BlogEntry.DoesNotExist:
        recent_entry = None
    return {'post': recent_entry}
