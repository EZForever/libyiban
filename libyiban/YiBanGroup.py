import re

from .YiBanArticle import YiBanArticle

class YiBanGroup:
    '''
    Handles group operations, provides factory for YiBanArticle.
    User should not create YiBanGroup instances manually;
    use YiBanAccount.get_groups() instead.
    '''
    
    def __init__(self, account, puid, gid):
        '''
        Initiate a new YiBanGroup instance.
            account - A YiBanAccount instance as the accessing identity.
            puid - The group's PUID, as seen in the URL.
            gid - The group's Group ID, as seen in the URL.
        '''
        self.puid = puid
        self.gid = gid
        
        self.account = account
        self.account.login()
        
        self.cid = self.__get_channelid()
    
    def __del__(self):
        self.account.logout()
        self.account = None
    
    def __repr__(self):
        return '<YiBanGroup#%x: puid = %d, gid = %d>' % (id(self), self.puid, self.gid)
    
    def __get_channelid(self):
        req = self.account.session.post('/forum/api/getListAjax', data = {
            'puid': self.puid,
            'group_id': self.gid
        })
        return int(req.json()["data"]["channel_id"])
    
    def get_egpa(self):
        '''
        Get the group's EGPA value as a float number.
        '''
        print('[I][Group] Getting EGPA value for %d:%d...' % (self.puid, self.gid))
        req = self.account.session.get('/newgroup/indexPub/group_id/%d/puid/%d' % (self.gid, self.puid))
        re_egpa = re.search('EGPA：(.*)<', req.text) # sic; note that full-width colon
        assert re_egpa, '[E][Group] EGPA value not found'
        return float(re_egpa.group(1))
    
    def get_articles(self, count):
        '''
        Get an iterator for (title, YiBanArticle) tuples.
        '''
        req = self.account.session.post('/forum/article/listAjax', data = {
            'puid': self.puid,
            'group_id': self.gid,
            'channel_id': self.cid,
            'size': count,
            'page': 1,
            'orderby': 'updateTime',
            'Sections_id': -1,
            'need_notice': 0,
            'my': 0
        })
        for item in req.json()['data']['list']:
            yield (item['title'], YiBanArticle(self.account, self.puid, self.cid, int(item['id'])))
    
    def new_article(self, title, content):
        '''
        Post a new article as the given identity.
            title - New article's title.
            content - New article's content, in raw HTML.
        Returns a (title, YiBanArticle) tuple.
        '''
        print('[I][Group] Post article w/ title "%s"' % title)
        req = self.account.session.post('/forum/article/addAjax', data = {
            'puid': self.puid,
            'pubArea': self.gid,
            'title': title,
            'content': content,
            'isNotice': 'false',
            'dom': '.js-submit'
        })
        req_json = req.json()
        assert req_json['code'] == 200, '[E][Group] Post article failed: ' + req.text
        url_parts = req_json['data']['link'].split('/')
        return (title, YiBanArticle(self.account, self.puid, self.cid, int(url_parts[5])))

