from django import template

register = template.Library()

@register.inclusion_tag('cinemaclubs/tags/comments.html')
def custom_comments_tree(obj):
    return {'obj': obj}
