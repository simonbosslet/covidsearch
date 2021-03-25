from django import template
from django.utils import safestring

register = template.Library()

@register.simple_tag
def convertLinks(message):
    words = message.split()
    for word in words:
        if word[0] == '(' and word[-1] == ')':
            word = word[1:-1]
            if word[0:4] == 'http':
                words[words.index(f'({word})')] = f'(<a href="{word}" target="_blank">{word}</a>)'
        elif word[0:4] == 'http':
            words[words.index(word)] = f'<a href="{word}" target="_blank">{word}</a>'
    message = ' '.join(words)

    return safestring.mark_safe(message)