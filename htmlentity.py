try:
    import htmlentitydefs
except: # python 3
    from html import entities as htmlentitydefs
import re
xed_re = re.compile(r'&#(\d+);') # for numberic entity
xed_re2 = re.compile(r'&(\w+);') # for named entity

def usub(m): return unichr(int(m.group(1))).encode('utf8')

def usub2(m):
    name = m.group(1)
    code = htmlentitydefs.name2codepoint.get(name, None)
    if not code:
        return '&%s;' %name

    return unichr(int(code)).encode('utf8')

#s = '&#227;, &#1606;, &#1588;'
#u = xed_re.sub(usub, s)
def html_entity_decode(s):
    s = xed_re2.sub(usub2, s)
    s = xed_re.sub(usub, s)
    return s

hex_re = re.compile(r'\\x([0-9a-zA-Z]+)')
def hex_sub(m): return unichr(int(m.group(1),16)).encode('utf8')
def hex_decode(s):
    s = hex_re.sub(hex_sub, s)
    return s

tags_re = re.compile(r'<([^>]+)>')
tags_re2 = re.compile(r'<([^>]+)$')
def tsub(m):
    return ''

def html_tags_strip(s, replacer=''):
    s = tags_re.sub(lambda m: replacer, s)
    s = tags_re2.sub(lambda m: replacer, s)
    return s

regex_p = re.compile("([!\"#\$%&\'\(\)\*\+,\-\.\/\:;\<\=\>\?\@\[\\\\\]\^_`\{\|\}~]+)")
regex_p2 = re.compile("([ !\"#\$%&\'\(\)\*\+,\-\.\/\:;\<\=\>\?\@\[\\\\\]\^_`\{\|\}~]+)")

def strip_punctuation(s):
    '''strip all punctuation in string'''
    if not s:
        s = ''
    return regex_p.sub(lambda m:'', s)

def strip_punctuation2(s):
    '''strip all punctuation in string including space.'''
    if not s:
        s = ''
    return regex_p2.sub(lambda m:'', s)

tags_space = re.compile(r'>(\s+)<')
def strip_space_between_tags(s):
    return tags_space.sub(lambda m: '><', s)

regex_ws = re.compile("([ \f\n\r\t\v]+)")
regex_ws2 = re.compile("([\f\n\r\t\v]+)")
def strip_whitespace(s):
    '''strip whitespace character including space, tab, form-feed, etc.'''
    return regex_ws.sub(lambda m: '', s)

def strip_whitespace2(s):
    '''strip whitespace character excluding space'''
    return regex_ws2.sub(lambda m: '', s)

regex_number = re.compile("([^0-9]+)")
def pick_number(s):
    if not s:
        s = ''

    return regex_number.sub(lambda m:'', s)

if __name__ == '__main__':
    s = '&amp;, &#39;, &#1588;, &unknown;, &lt;, &gt;'
    print (html_entity_decode(s))

    c = u'Bakery, Panader?a, Restaurant &amp; Caribbean, Bakers-Retail, Restaurants'
    print (html_entity_decode(c))

    d = 'http://maps.google.com/maps/place?um=1&amp;ie=UTF-8&amp;q=McDonalds,+New+York&amp;fb=1&amp;gl=us&amp;hq=McDonalds,&amp;hnear=New+York,+NY&amp;cid=15520961891315400286&amp;ei=7RAwTdGaE5LEsAPBusiLBg&amp;sa=X&amp;oi=local_result&amp;ct=placepage-link&amp;resnum=2&amp;ved=0CCsQ4gkwAQ'
    print (html_entity_decode(d))

    t = '<span class=f><cite><b>twitter</b>.com/<b>cornerbistro</b></cite>'
    print (html_tags_strip(t))

