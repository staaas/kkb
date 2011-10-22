from datetime import datetime, timedelta

from django import template
from django.utils.formats import date_format
from django.utils import dateformat
from django.utils.translation import ugettext as _

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

_DATE_STR_FORMAT = '%Y%m%d'

@register.filter(name='display_date')
def _base_display_date(date, display_func):
    '''
    Returns date represented as a fancy string to be
    displayed at calendar page.
    '''
    now = datetime.now()
    if date.strftime(_DATE_STR_FORMAT) == now.strftime(_DATE_STR_FORMAT):
        return display_func(_(u"Today"))
    tomorrow = now + timedelta(days=1)
    if date.strftime(_DATE_STR_FORMAT) == tomorrow.strftime(_DATE_STR_FORMAT):
        return display_func(_(u"Tomorrow"))
    return display_func(date_format(date, format='MONTH_DAY_FORMAT'))

@register.filter(name='display_date')
def display_date(date):
    return _base_display_date(date, lambda x: x)

@register.filter(name='display_date_with_comma')
def display_date_with_comma(date):
    return _base_display_date(date, lambda x: '%s,' % x)

@register.filter(name='display_date_and_weekday')
def display_date_and_weekday(date):
    def display_func(date_as_text):
        return '%s, %s' % (date_as_text,
                           dateformat.format(date, 'l'))
    return _base_display_date(date, display_func)
