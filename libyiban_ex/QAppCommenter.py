

class QAppCommenter:
    '''
    Provides commenting ability to YiBan QApps.
    This is an example of extending libyiban's functionality.
    '''
    
    def __init__(self, account, appid):
        '''
        Initiate a new YiBanArticle instance.
            account - A YiBanAccount instance as the accessing identity.
            app - The QApp's ID, as seen in the URL.
        '''
        self.appid = appid
        self.account = account
        self.account.login()
        
        # self.account.session has a default host of 'https://yiban.cn/', which can be overridden
        req = self.account.session.get('https://q.yiban.cn/app/getAllConfigAjax?appid=%d' % self.appid)
        req_json = req.json()
        assert req_json['code'] == 200, '[F][QApp] Get app config failed: ' + req.text
        self.__code = next((x['code'] for x in req_json['data']['allConfig'] if x['type'] == 'extendcomment'), None)
        assert self.__code != None, '[F][QApp] App has no comment section available'
    
    def __del__(self):
        self.account.logout()
        self.account = None
        
    def __repr__(self):
        return '<QAppCommenter#%x: appid = %d>' % (id(self), self.appid)
    
    def new_comment(self, content):
        '''
        Post a new comment as the given identity.
            content - Comment content.
        '''
        print('[I][QApp] Comment on QApp %d' % self.appid)
        self.account.session.post('https://q.yiban.cn/comment/addComment', data = {
            'appid': self.appid,
            'App_id': self.appid,
            'type': 'extendcomment',
            'code': self.__code,
            'title': 'YIBAN_NEVER_CHECK_THIS_TITLE',
            'content': content,
            'isAnonymous': 1,
            'isFeed': 2
        })

