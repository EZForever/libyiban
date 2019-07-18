import requests
import re

def get_articles(oCookie, puid, gid, channelid, count):
    print("[I][Arti] Fetch first at most %d articles" % count)
    rArti = requests.post("https://www.yiban.cn/forum/article/listAjax", cookies = oCookie, data = {
        "puid": puid,
        "group_id": gid,
        "channel_id": channelid,
        "size": count,
        "page": 1,
        "orderby": "updateTime",
        "Sections_id": -1,
        "need_notice": 0,
        "my": 0
    })
    aRet = []
    for oItem in rArti.json()["data"]["list"]:
        # (channelid, articleid, sTitle)
        aRet.append((int(oItem["Channel_id"]), int(oItem["id"]), oItem["title"]))
    return aRet

def get_replies(oCookie, puid, channelid, articleid, count):
    print("[I][Arti] Fetch first at most %d replies" % count)
    rArti = requests.post("https://www.yiban.cn/forum/reply/listAjax", cookies = oCookie, data = {
        "puid": puid,
        "channel_id": channelid,
        "article_id": articleid,
        "size": count,
        "page": 1,
        "order": 1
    })
    oItems = rArti.json()["data"]
    aRet = [oItems["list"]["article"]["title"]]
    for i in range(min(iNum, oItems["count"])):
        aRet.append(oItems["list"][str(i)]["content"])
    return aRet

def like(oCookie, puid, channelid, articleid):
    print("[I][Arti] Like article %d" % articleid)
    requests.post("https://www.yiban.cn/forum/article/upArticleAjax", cookies = oCookie, data = {
        "puid": puid,
        "channel_id": channelid,
        "article_id": articleid
    })

def reply(oCookie, puid, channelid, articleid, sContent):
    print("[I][Arti] Reply article %d with '%s'" % (articleid, sContent))
    requests.post("https://www.yiban.cn/forum/reply/addAjax", cookies = oCookie, data = {
        "puid": puid,
        "channel_id": channelid,
        "article_id": articleid,
        "content": sContent,
        "reply_id": 0,
        "syncFeed": 0,
        "isAnonymous": 0
    })

def post(oCookie, puid, gid, sTitle, sContent):
    print("[I][Arti] Post article with title '%s'" % sTitle)
    rPost = requests.post("https://www.yiban.cn/forum/article/addAjax", cookies = oCookie, data = {
        "puid": puid,
        "pubArea": gid,
        "title": sTitle,
        "content": sContent,
        "isNotice": "false",
        "dom": ".js-submit"
    })
    if rPost.json()["code"] != 200:
        print("[F][Arti] Post article failed: ", rPost.json())
        return None
    aElems = rPost.json()["data"]["link"].split("/")
    # Same as in get_articles()
    return (int(aElems[7]), int(aElems[5]), sTitle)

