import requests
import base64
import rsa # pip install rsa
import re
import io

from PIL import Image

def login(sUsername, sPassword):
    print("[I][Auth] Logging in with YiBan account %s" % sUsername)

    rLoginPage = requests.get("https://www.yiban.cn/login")
    try:
        sPubKey = re.search("data-keys='(.*)'", rLoginPage.text, flags = re.M | re.S).group(1)
        sPubKeyTime = re.search("data-keys-time='(.*)'", rLoginPage.text).group(1)
    except AttributeError:
        print("[F][Auth] Login failed: No public key")
        return None
    oPubKey = rsa.PublicKey.load_pkcs1_openssl_pem(sPubKey.encode())

    bReqCaptcha = False
    while True:
        if bReqCaptcha:
            try:
                sCaptchaID = re.search('/captcha/index\?(\d+)', rLoginPage.text).group(1)
            except AttributeError:
                print("[F][Auth] Login failed: No captcha")
                return None
            rCaptcha = requests.get("https://www.yiban.cn/captcha/index?%s" % sCaptchaID, cookies = rLoginPage.cookies)
            with io.BytesIO(rCaptcha.content) as f:
                Image.open(f).show()
            sCaptcha = input("[?][Auth] Input captcha: ")
        else:
            sCaptcha = ""
        rYBAuth = requests.post("https://www.yiban.cn/login/doLoginAjax", allow_redirects = False, cookies = rLoginPage.cookies, data = {
            "account": sUsername,
            "password": base64.b64encode(rsa.encrypt(sPassword.encode(), oPubKey)).decode(),
            "captcha": sCaptcha,
            "keysTime": sPubKeyTime
        })
        if rYBAuth.json()["code"] == "711":
            print("[I][Auth] Captcha required. Attempt re-login.")
            bReqCaptcha = True
        elif rYBAuth.json()["code"] != 200: # sic; stupid backend developers
            print("[F][Auth] Login failed: ", rYBAuth.json())
            return None
        else:
            break
    return rYBAuth.cookies

def logout(oCookie):
    print("[I][Auth] Logging out")
    requests.get("https://www.yiban.cn/logout", cookies = oCookie)

