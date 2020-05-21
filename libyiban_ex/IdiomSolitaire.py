import requests
import random
import re

class IdiomSolitaire:
    '''
    Idiom solitaire solver.
    Data credit: http://www.jielongdaquan.com/
    '''
    
    # Default idioms when no solitaire available
    DEFAULT_IDIOMS = [
        '约定俗成', '心照不宣', '墨守成规', '火树银花'
    ]
    
    def __init__(self, initial):
        '''
        Initiate a new IdiomSolitaire instance.
            initial - The idiom, word or sentence to start with.
        '''
        self.__state = initial[-1]
    
    def get(self):
        '''
        Get next idiom. If no solitaire found, returns a random idiom from
        IdiomSolitaire.DEFAULT_IDIOMS list.
        '''
        req = requests.get('http://www.jielongdaquan.com/phrase/1/%s.aspx' % self.__state.encode().hex())
        req.encoding = 'utf-8'
        idioms_html = re.search('<ul class="phrase" id="content">(.*?)</ul>', req.text, flags = re.M | re.S).groups(1)[0]
        idioms = re.findall('<a.*?>\s*(.*?)\s*</a>', idioms_html, flags = re.M | re.S) or self.__class__.DEFAULT_IDIOMS
        idiom = random.choice(idioms)
        self.__state = idiom[-1]
        return idiom

