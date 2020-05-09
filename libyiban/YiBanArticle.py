

class YiBanArticle:
    
    def __init__(self, account, puid, cid, aid):
        self.puid = puid
        self.cid = cid
        self.aid = aid
        self.account = account
        self.account.login()
    
    def __del__(self):
        self.account.logout()
        self.account = None
        
    def __repr__(self):
        return '<YiBanArticle#%x: cid = %d, aid = %d>' % (id(self), self.cid, self.aid)
    
    def like(self):
        print('[I][Article] Like article %d:%d' % (self.cid, self.aid))
        self.account.session.post('/forum/article/upArticleAjax', data = {
            'puid': self.puid,
            'channel_id': self.cid,
            'article_id': self.aid
        })
    
    def get_content(self):
        req = self.account.session.post('/forum/article/showAjax', data = {
            'puid': self.puid,
            'channel_id': self.cid,
            'article_id': self.aid,
            'origin': 0
        })
        data = req.json()['data']['article']
        return (data['title'], data['content'])
    
    def get_replies(self, count):
        print('[I][Article] Getting first at most %d replies' % count)
        req = self.account.session.post('/forum/reply/listAjax', data = {
            'puid': self.puid,
            'channel_id': self.cid,
            'article_id': self.aid,
            'size': count,
            'page': 1,
            'order': 1
        })
        items = req.json()['data']
        for i in range(min(count, items['count'])):
            yield items['list'][str(i)]['content']
    
    def new_reply(self, content, anonymous = False):
        print('[I][Article] Reply article %d:%d' % (self.cid, self.aid))
        self.account.session.post('/forum/reply/addAjax', data = {
            'puid': self.puid,
            'channel_id': self.cid,
            'article_id': self.aid,
            'content': content,
            'reply_id': 0,
            'syncFeed': 0,
            'isAnonymous': 1 if anonymous else 0
        })
