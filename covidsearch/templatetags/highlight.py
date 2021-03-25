from django import template
from django.utils import safestring
import re

register = template.Library()

@register.simple_tag
def highlight(query, message, convertLinks= True):
    words = message.split()
    for i in words:
        if 'http' in i and convertLinks:
            words = message.split()
            for word in words:
                if 'a' and 'http' in word:
                    newword = ''.join(words[words.index(word):words.index(word)+1])
                if '(' in word or ')' in word:
                    newword = word.replace('(', '')
                    newword = newword.replace(')', '')
                    if newword[0:4] == 'http':
                        words[words.index(f'{word}')] = f'(<a href="{newword}" target="_blank">{newword}</a>)'
                elif word[0:4] == 'http':
                    words[words.index(word)] = f'<a href="{word} target="_blank"">{word}</a>'
            message = ' '.join(words)
    if message == query:
        message = f'<span id="query-highlight">{message}</span>'
    elif len(query) == 1:
        for i in words:
            counter = 0
            for a in i:
                if a.upper() == query.upper():
                    counter += 1
            if counter > 1:
                place = 0
                letters = [char.upper() for char in i]
                good_letters = [char for char in i]
                letterlist = []
                wordslist = []
                for c in letters:
                    if c in letterlist:
                        good_letters[place] = f'<span id="query-highlight">{good_letters[place]}</span>'
                        d = ''.join(good_letters)
                        words[words.index(wordslist[letterlist.index(c)])] = d
                        wordslist[letterlist.index(c)] = d
                        
                    elif letters[place] == query.upper():
                        good_letters[place] = f'<span id="query-highlight">{good_letters[place]}</span>'
                        d = ''.join(good_letters)
                        words[words.index(i)] = d
                        letterlist.append(c)
                        wordslist.append(d)
                    place += 1
            else:
                letters = [char.upper() for char in i]
                good_letters = [char for char in i]
                for c in letters:
                    if c == query.upper():
                        good_letters[letters.index(c)] = f'<span id="query-highlight">{good_letters[letters.index(c)]}</span>'
                        c = ''.join(good_letters)
                        words[words.index(i)] = c
        message = ' '.join(words)
            
    elif len(words) == 1:
        letters = [char.upper() for char in message]
        querychars = [char.upper() for char in query]
        good_letters = [char for char in message]
        place = 0
        for i in letters:
            if i == querychars[0]:
                if len(letters[place:]) >= len(querychars):
                    if letters[place:place+len(querychars)] == querychars:
                        good_letters[place+len(querychars)-1] += '</span>'
                        good_letters[place] = f'<span id="query-highlight">{good_letters[place]}'
                        message = ''.join(good_letters)
            place += 1
        message = ''.join(message)
    
    elif ' ' not in query:
        for a in words:
            letters = [char.upper() for char in a]
            good_letters = [char for char in a]
            querychars = [char.upper() for char in query]
            letterlist = []
            wordslist = []
            place = 0
            for i in letters:
                if i == querychars[0]:
                    if len(letters[place:]) >= len(querychars):
                        if letters[place:place+len(querychars)] == querychars:
                            if querychars in letterlist:
                                good_letters[place+len(querychars)-1] += '</span>'
                                good_letters[place] = f'<span id="query-highlight">{good_letters[place]}'
                                d = ''.join(good_letters)
                                
                            else:
                                good_letters[place+len(querychars)-1] += '</span>'
                                good_letters[place] = f'<span id="query-highlight">{good_letters[place]}'
                                d = ''.join(good_letters)
                                words[words.index(a)] = d
                                letterlist.append(letters[place:place+len(querychars)])
                                wordslist.append(d)
                                
                place += 1
    
        message = ' '.join(words)
                    
    else:
        letters = [char.upper() for char in message]
        querychars = [char.upper() for char in query]
        good_letters = [char for char in message]
        place = 0
        for i in letters:
            if i == querychars[0]:
                if len(letters[place:]) >= len(querychars):
                    if letters[place:place+len(querychars)] == querychars:
                        good_letters[place+len(querychars)-1] += '</span>'
                        good_letters[place] = f'<span id="query-highlight">{good_letters[place]}'
                        message = ''.join(good_letters)
            place += 1
        message = ''.join(message)
    return safestring.mark_safe(message)
