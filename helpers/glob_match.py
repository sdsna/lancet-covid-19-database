# Adapted from: https://stackoverflow.com/a/29820981
# Test if the string matches the given glob

import re

def glob_match(glob, string):
    return re.match(glob_to_regex(glob), string)

def glob_to_regex(glob):
    """Translate a shell PATTERN to a regular expression.

    There is no way to quote meta-characters.
    """

    i, n = 0, len(glob)
    regex = ''
    while i < n:
        c = glob[i]
        i = i+1
        if c == '*':
            #regex = regex + '.*'
            regex = regex + '[^/]*'
        elif c == '?':
            #regex = regex + '.'
            regex = regex + '[^/]'
        elif c == '[':
            j = i
            if j < n and glob[j] == '!':
                j = j+1
            if j < n and glob[j] == ']':
                j = j+1
            while j < n and glob[j] != ']':
                j = j+1
            if j >= n:
                regex = regex + '\\['
            else:
                stuff = glob[i:j].replace('\\','\\\\')
                i = j+1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                regex = '%s[%s]' % (regex, stuff)
        else:
            regex = regex + re.escape(c)
    return regex + '\Z(?ms)'
