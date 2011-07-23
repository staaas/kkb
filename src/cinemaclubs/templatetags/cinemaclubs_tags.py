from django import template

from cinemaclubs.utils import socialize_users

register = template.Library()

@register.inclusion_tag('cinemaclubs/tags/comments.html', takes_context=True)
def custom_comments_tree(context, obj):
    return {'obj': obj,
            'request': context['request']}

@register.inclusion_tag('cinemaclubs/tags/display_user.html')
def display_user(user):
    if not hasattr(user, 'soc_provider'):
        # the user hasn't been socialized yet
        socialize_users(user)
    return {'user': user}

@register.filter(name='populate_users')
def populate_users(comment_list):
    socialize_users(*[cmt.user for cmt in comment_list])
    return comment_list
