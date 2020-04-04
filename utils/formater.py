import re


def markdown_v2_formater(text):
    escaped_char = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    def multiple_replace(text, adict):  
        rx = re.compile('|'.join(map(re.escape, adict)))  
        def one_xlat(match):  
            return adict[match.group(0)]  
        return rx.sub(one_xlat, text)
    edict = {}
    for i in escaped_char:
        edict.update({i: '\\' + i})
    text = multiple_replace(text, edict)
    return text