from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag(takes_context=True)
def my_error_messages(context):
    messages = context.get('messages')
    if not messages:
        return ''
    html = ''
    for message in messages:
        if message.tags == 'error':
            html += '<p class="my-error">%s</p>' %message
    return mark_safe(html)
