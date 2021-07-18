# url_replace.py
# https://stackoverflow.com/a/62587351/802542
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    if kwargs.get('page'):
        query.pop('page', None)
    if kwargs.get('ordering'):
        query.pop('ordering', None)
    query.update(kwargs)
    return query.urlencode()