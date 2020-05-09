from enum import Enum

import requests
import json

class CATEGORY(Enum):
    POLITICS = 113352
    LOCAL = 113321
    LEGAL = 113207
    TECH = 11109303
    ENG_SCITECH_INTERNET = 11143428
    EDUCATION = 11209936

def get(category, count = 1):
    print('[I][XinHuaNews] Fetching %d article(s) from category %s' % (count, category.name))
    req = requests.get('http://qc.wa.news.cn/nodeart/list?nid=%d&pgnum=1&cnt=%d&tp=1&orderby=1' % (category.value, count))
    req.encoding = 'utf-8'
    entries = json.loads(req.text[1:-1])['data']['list']
    articles = []
    for entry in entries:
        # XXX: Move this 'decoration' section to an example and just return (title, abstract, url)?
        content = '<p>%s<a href="%s">阅读全文&gt;&gt;</a></p>' % (entry['Abstract'], entry['LinkUrl'])
        articles.append((entry['Title'], content))
    return articles

