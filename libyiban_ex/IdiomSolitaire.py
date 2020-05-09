import requests
import random
import re

class IdiomSolitaire:
    
    # Default idioms when no solitaire available
    DEFAULTS = [
        '约定俗成', '心照不宣', '墨守成规', '火树银花'
    ]
    
    def __init__(self, initial):
        self.__state = initial[-1]
    
    def get(self):
        req = requests.get('http://www.jielongdaquan.com/phrase/1/%s.aspx' % self.__state.encode().hex())
        req.encoding = 'utf-8'
        idioms_html = re.search('<ul class="phrase" id="content">(.*?)</ul>', req.text, flags = re.M | re.S).groups(1)[0]
        idioms = re.findall('<a.*?>\s*(.*?)\s*</a>', idioms_html, flags = re.M | re.S) or self.__class__.DEFAULTS
        idiom = random.choice(idioms)
        self.__state = idiom[-1]
        return idiom

