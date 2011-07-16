from django import template

register = template.Library()

@register.inclusion_tag('cinemaclubs/tags/comments.html', takes_context=True)
def custom_comments_tree(context, obj):
    return {'obj': obj,
            'request': context['request']}
