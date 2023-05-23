import time
import random
import requests

url = "https://otheve.beacon.qq.com/analytics/upload?tp=js"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    # "Content-Length: 851    "Content-Type": "application/json;charset=UTF-8",    "Host": "otheve.beacon.qq.com",
    "Origin": "https://news.qq.com",
    "Referer": "https://news.qq.com/hdh5/bank2020.htm",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

data = {"deviceId": "5fc808f8c3ce83057f7a257b094e0240", "appkey": "JS0ZOQ2M3YR2SC", "versionCode": "0.1.0",
        "initTime": "1599011920940", "channelID": "web", "sdkVersion": "3.1.50-web", "pixel": "1920*1080*1",
        "language": "en", "msgs": [{"type": 2,
                                    "data": {"id": "JS0ZOQ2M3YR2SC_1599011920940", "start": 1599011920940, "pages": [],
                                             "status": 2, "duration": 0, "events": [
                                            {"id": "rmb_view_poster", "name": "rmb_view_poster",
                                             "params": {"provinceName": "ËÄ´¨Ê¡", "cityName": "³É¶¼ÊÐ",
                                                        "cityOrRural": "³ÇÊÐ", "appversion": "unknown",
                                                        "phoneversion": "otherOS", "appnetwork": "unknown",
                                                        "phonemodel": "unknown", "phonesystem": "unknown",
                                                        "deviceid": "unknown", "openid": "unknown", "omgid": "unknown",
                                                        "uid": "unknown", "qquin": "unknown", "openFrom": "",
                                                        "A102": "https://news.qq.com/hdh5/bank2020.htm#/",
                                                        "A104": "https://huitongjinrong.wjx.cn/jq/87921730.aspx",
                                                        "A99": "Y", "A100": 5}, "start": 1599012097622, "count": 1}]}}]}

for i in range(2000):
    print(i)
    init = (int(time.time() * 1000))
    end = init + random.randint(100000, 150000)

    data["initTime"] = str(init)
    data["msgs"][0]["data"]["id"] = f"JS0ZOQ2M3YR2SC_{str(init)}"
    data["msgs"][0]["data"]["start"] = init
    data["msgs"][0]["data"]["events"][0]["start"] = end
    resp = requests.post(url, headers=headers, data=data)
    print(resp.status_code)
    time.sleep(1)