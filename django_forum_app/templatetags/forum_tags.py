from django import template

register = template.Library()

@register.filter
def check_seen(obj, user):
    return obj.has_seen(user)
