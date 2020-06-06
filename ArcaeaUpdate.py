import random
import time
import winsound

import requests
import win32api
import win32con
from lxml import etree

headers = {
    'Host': 'arcaea.lowiro.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'Cookie': '_ga=GA1.2.1746628465.1571674925; __stripe_mid=d185df61-83c0-47d1-8760-dcdd6dda94e4; ctrcode=CN; resolution=1536; _gid=GA1.2.273463961.1579585090; XSRF-TOKEN=eyJpdiI6ImE5QVRMUmdtdzlCWXNUc09SUHROcVE9PSIsInZhbHVlIjoiXC9zaFlxYjcyZzI2Skx0RFRKTFVtZWJ3ejA2dFV2MmVYR3A0NlV2eWJrMDVibldyUE80RTlmY2FOU3FldWMwYktlNUVxR1BVdEVEMGZEcFF3TDc5YmdRPT0iLCJtYWMiOiJkNzcxNGM5OGZkNmNlYTM2ZmEyODQwNDYyNjA1ODdmMGI2MWE0MTFlMWU3NTdmYmYyNTkwNjhlYjUxNmJhNWEzIn0%3D; laravel_session=eyJpdiI6ImJoR3dmNWdTNU5vWTk5ZVpleXo5SWc9PSIsInZhbHVlIjoidVhmOUhFeDVpM0dUeUhIUU1zMkxNcXdpSkdpYTd5VlFVanduZGVjekUwMkg2cjV5XC9HXC9peHVKVDh5cDdzb3JhSGEwSWtXVXZlc2RUUndNc0ZTckFJQT09IiwibWFjIjoiNjUwYTE1ZGEwOTUwN2EzODcyOTAwMTZlMzBhMDM5MjBjODY0Y2E2ODczOTU2NDhlOTY2OGNkMTRhYzFlMTQ5OSJ9; _gat=1'
}


def update():
    url = [
        'https://arcaea.lowiro.com/ja',
        'https://arcaea.lowiro.com/zh'
    ]
    r = requests.get(url[random.randint(0, 1)], headers=headers).text
    select = etree.HTML(r)
    content = select.xpath('//div[@class="link-wrapper hide-country"]/a/@href')
    downurl = 'https://static-lb.lowiro.com/serve/arcaea_2.4.9c.apk?token=tQKQZ8KMutR4T9MqaT4E2Ls7Qepu8HaaXh280LQlfyHMQf03WeC1MFQnaBvJA4B6G'
    downurl = 'https://static-lb.lowiro.com/serve/arcaea_2.6.2c.apk?token=yenuObL2DzPMoVJTAdBRlfVz0myISrZhthc5l8Yv0abLHVXfpLBWOOyKrVcY7e3BQ'
    downurl = 'https://static-lb.lowiro.com/serve/arcaea_2.6.2c.apk?token=c9nDgyEFJAXnvRzgEjJCLD4rysAYrzAo4Dlwhc4yncFuXknsFBZuPCDOPnjG1DSta'
    if content[0] != downurl:
        print(content[0])
        winsound.Beep(750, 3500)
        return 0
    else:
        print(time.strftime("%Y{}%m{}%d{} %H:%M:%S", time.localtime()).format('年', '月', '日') + '还没更新')
        return 1


while True:
    if update() == 1:
        time.sleep(25)
    else:
        # 重试信息框
        while True:
            if win32api.MessageBox(0, "更新啦！！！", "提醒", win32con.MB_RETRYCANCEL):
                continue
            else:
                break
