from django.shortcuts import get_object_or_404

from commonutils.decorators import render_to
from models import BlogEntry

@render_to('blog/post_detail.html')
def post_detail(request, year, month, day, slug):
    year, month, day = int(year), int(month), int(day)
    post = get_object_or_404(BlogEntry, slug=slug, published=True)
    # redirect

    return {'post': post}

@render_to('blog/posts.html')
def posts(request):
    posts_qs = BlogEntry.objects.filter(published=True).order_by('-published_at')
    return {'posts': list(posts_qs)}
