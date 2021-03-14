from django import template

register = template.Library()

@register.simple_tag
def replace(query, message):
    return message.replace(query, f'<span id="query-highlight">{query}</span>')