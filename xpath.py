# -*- coding: utf-8 -*-
import lxml.html
from lxml import etree
import re

import sys
sys.path.append('..')
from htmlentity import html_entity_decode

img_re = re.compile(r'<img([^>]+)>')
def clear_img_tag(s):
    return img_re.sub(lambda m: '', s)

script_re = re.compile(r'<script([^>]*)>.*?<\/script>')
def clear_script_tag(s):
    return script_re.sub(lambda m: '', s)

def search(html, xpath):
    try:
        html = html.encode('utf-8')
    except:
        pass
    doc = lxml.html.fromstring(html)
    r = doc.xpath(xpath)
    return r

def inner_html(node, clear_img=True, decode_html_entity=True):
    html = str(etree.tostring(node, encoding='ASCII'))
    if clear_img:
        html = clear_img_tag(html)

    #if decode_html_entity:
    #    html = html_entity_decode(html)
    #    try:
    #        html = html.decode('ascii')
    #    except:
    #        pass

    #print(html)
    return html

if __name__ == '__main__':
    s= u'<span class="_Xbe kno-fv">Tradição e Pioneirismo na Educação (Tradition and Pioneering in Education, <a class="fl" href="/search?q=Portuguese&amp;stick=H4sIAAAAAAAAAOPgE-LUz9U3sDDMKKtS4gAxTauyUrTUMsqt9JPzc3JSk0sy8_P084vSE_MyqxJBnGKrosRyhdz8kpJ8ACHZfkE_AAAA&amp;sa=X&amp;ved=0ahUKEwjwtLL5k8bSAhWnxFQKHQCLD2oQmxMImwEoATAY" data-ved="0ahUKEwjwtLL5k8bSAhWnxFQKHQCLD2oQmxMImwEoATAY">Portuguese Language</a>)</span>'
    e = search(s, '//span')
    print (inner_html(e[0]))
    sys.exit(0)

    import urllib2

    headers = {
        'User-Agent':'	Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.25) Gecko/20111212 AlexaToolbar/alxf-1.54 Firefox/3.6.25 GTB7.1',
        'Accept':'*/*',
        'Connection': 'keep-alive'
    }
    opener = urllib2.build_opener() ##urllib2.ProxyHandler({'http': '127.0.0.1:3998'}))
    url = "http://www.linkedin.com/company/10-10-chile" #"http://www.bing.com/search?q=%22148apps.com%22+site%3Alinkedin.com"
    request = urllib2.Request(url, headers=headers)
    request.set_proxy('127.0.0.1:3998', 'http')
    file = opener.open(request)
    html = file.read()
    #print html
    #results = search(html, '//li[@class="sa_wr"]//h3/a[1]')
    results = search(html, '//dd[preceding-sibling::dt[1]="Website"]/a[1]')
    print (results)
    if results:
        for item in results:
            print (item.text_content())
