import requests
import re

def checkin(oCookie):
    print("[I][Misc] Checking in")
    rCheckIn = requests.post("https://www.yiban.cn/ajax/checkin/answer?optionid[]=6713", cookies = oCookie)
    # Note this won't give you as much score as answering the daily question.
    # The following unfinished code does that.
    '''
    rCheckInQ = requests.get("https://mobile.yiban.cn/api/v3/checkin/question?access_token=%s" % oCookie["yiban_user_token"])
    if rCheckInQ.json()["response"] != 100:
        print("[E] Error fetching checkin info")
    else if rCheckInQ.json()["data"]["has_survey"] && !rCheckInQ.json()["data"]["isChecked"]:
        rCheckInA = requests.post("https://mobile.yiban.cn/api/v3/checkin/answer?access_token=%s&optionId=%s" % (oC["yiban_user_token"], rCheckInQ.json()["data"]["survey"]["question"]["option"][0]["id"]))
    '''

def get_egpa(oCookie, puid, gid):
    print("[I][Misc] Fetch EGPA of %d:%d" % (puid, gid))
    rGroup = requests.get("https://www.yiban.cn/newgroup/indexPub/group_id/%d/puid/%d" % (gid, puid), cookies = oCookie)
    try:
        # sic; note that Chinese colon
        return float(re.search("EGPA：(.*)<", rGroup.text).group(1))
    except AttributeError:
        print("[E][Misc] Fetch failed: No EGPA value")
        return -1.0

def get_channelid(oCookie, puid, gid):
    rCID = requests.post("https://www.yiban.cn/forum/api/getListAjax", cookies = oC, data = {
        "puid": puid,
        "group_id": gid
    })
    return int(rCID.json()["data"]["channel_id"])

# msgid: 2 = System，3 = Friend Request，4 = Moments
def cleanmsg(oCookie, msgid):
    print("[I][CleanMsg] Start cleaning ID %d" % msgid)
    while True:
        rMsg = requests.get("https://www.yiban.cn/message/index/type/%d" % msgid, cookies = oCookie)
        rMsg.encoding = 'utf-8'
        aMsg = re.findall('data-id="([0-9a-f]{24})" data-content="(.*?)">', rMsg.text)
        if len(aMsg) == 0:
            break
        print("[I][CleanMsg] Found %d Messages" % len(aMsg))

        oData = {}
        for i in range(len(aMsg)):
            oData["messages[%d][id]" % i] = aMsg[i][0]
            oData["messages[%d][content]" % i] = aMsg[i][1]
        oData["option"] = "delete"
        oData["type"] = msgid
        rRes = requests.post("https://www.yiban.cn/message/batchAjax", cookies = oCookie, data = oData)
        if rRes.json()["code"] != 200:
            print("[E][CleanMsg] Error cleaning: ", end = "")
            print(rRes.json())
            break
    print("[I][CleanMsg] Clean complete")

