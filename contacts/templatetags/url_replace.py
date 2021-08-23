# url_replace.py
# https://stackoverflow.com/a/62587351/802542
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for e in ['pag', 'col', 'ord', 'p_by']:
        if kwargs.get(e):
            query.pop(e, None)
    query.update(kwargs)
    return query.urlencode()