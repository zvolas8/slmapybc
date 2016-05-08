from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    path = request.path
    if pattern in path:
        return 'active'
    return ''