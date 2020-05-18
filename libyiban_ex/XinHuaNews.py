'''xinhuanet.com news crawler.'''
from enum import Enum

import requests
import json

class CATEGORY(Enum):
    '''
    Available news' categories for XinHuaNews.get().
    '''
    POLITICS = 113352
    LOCAL = 113321
    LEGAL = 113207
    TECH = 11109303
    ENG_SCITECH_INTERNET = 11143428
    EDUCATION = 11209936

def get(category, count = 1):
    '''
    Get an iterator for (title, abstract, URL) tuples.
        category - A XinHuaNews.CATEGORY instance.
        count - Maximum number of iterated entries.
    '''
    print('[I][XinHuaNews] Fetching %d article(s) from category %s' % (count, category.name))
    req = requests.get('http://qc.wa.news.cn/nodeart/list?nid=%d&pgnum=1&cnt=%d&tp=1&orderby=1' % (category.value, count))
    req.encoding = 'utf-8'
    entries = json.loads(req.text[1:-1])['data']['list']
    for entry in entries:
        yield (entry['Title'], entry['Abstract'] or '', entry['LinkUrl'])

