from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    path = request.path
    if pattern in path:
        return 'active'
    return ''

@register.filter(name='range')
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)

@register.filter
def index(List, i):
    return List[int(i)]

