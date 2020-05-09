import requests_toolbelt.sessions
import PIL.Image
import getpass
import base64
import rsa
import re
import io

from .YiBanGroup import YiBanGroup

class YiBanAccount:
    
    def __init__(self, username = None, password = None):
        self.__refcnt = 0
        self.session = None
        
        if username is None:
            username = input('[?][Account] Input username: ')
        self.username = username
        
        if password is None:
            password = getpass.getpass('[?][Account] Input password for "%s": ' % username)
        self.__password = password
    
    def __del__(self):
        while self.__refcnt > 0:
            self.__release()
    
    def __enter__(self):
        self.__addref()
        return self
    
    def __exit__(self, type, value, trace):
        self.__release()
    
    def __repr__(self):
        return '<YiBanAccount#%x: username = %s>' % (id(self), self.username)
    
    def __assert_logged_in(self):
        assert self.__refcnt > 0, '[E][Account] Invalid operation: not logged in'
    
    def __real_login(self):
        print('[I][Account] Logging in...')
        self.session = requests_toolbelt.sessions.BaseUrlSession(base_url = 'https://www.yiban.cn/')
        
        req_login = self.session.get('/login')
        re_key = re.search("data-keys='(.*)'", req_login.text, flags = re.M | re.S)
        re_keytime = re.search("data-keys-time='(.*)'", req_login.text)
        assert re_key and re_keytime, '[F][Account] Login failed: public key not found'
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(re_key.group(1).encode())
        
        require_captcha = False
        while True:
            if require_captcha:
                re_captcha = re.search('/captcha/index\?(\d+)', req_login.text)
                assert re_captcha, '[F][Account] Login failed: captcha not found'
                req_captcha = self.session.get('/captcha/index?%s' % re_captcha.group(1))
                with io.BytesIO(req_captcha.content) as f:
                    PIL.Image.open(f).show()
                captcha_text = input('[?][Account] Input captcha: ')
            else:
                captcha_text = ''
            
            req_auth = self.session.post('/login/doLoginAjax', allow_redirects = False, data = {
                'account': self.username,
                'password': base64.b64encode(rsa.encrypt(self.__password.encode(), pubkey)).decode(),
                'captcha': captcha_text,
                'keysTime': re_keytime.group(1)
            })
            req_auth_json = req_auth.json()
            if req_auth_json['code'] == '711': # sic; stupid backend developers
                print("[I][Account] Captcha required. Retrying.")
                require_captcha = True
            else:
                assert req_auth_json['code'] == 200, '[F][Account] Login failed: ' + req_auth.text
                break
    
    def __real_logout(self):
        print('[I][Account] Logging out...')
        self.session.get('/logout')
        self.session = None
    
    def __addref(self):
        if self.__refcnt == 0:
            self.__real_login()
        self.__refcnt += 1
    
    def __release(self):
        self.__assert_logged_in()
        self.__refcnt -= 1
        if self.__refcnt == 0:
            self.__real_logout()
    
    def login(self):
        self.__addref()
    
    def logout(self):
        self.__release()
    
    def checkin(self):
        self.__assert_logged_in()
        print('[I][Account] Checking in...')
        self.session.post('/ajax/checkin/answer?optionid[]=6713')
    
    def get_groups(self):
        self.__assert_logged_in()
        req_group = self.session.get('/my/group')
        for gid, puid, name in re.findall('<a href="/newgroup/indexPub/group_id/(\d+)/puid/(\d+)"><span>(.*?)</span></a>', req_group.text):
            yield (name, YiBanGroup(self, int(puid), int(gid)))

