import requests
import re
import json


def getVideo(path, name, videoUrl):
    print('开始下载视频文件')
    file_path = path + name + '.mp4'
    pre_content_length = 0
    res = requests.get(videoUrl, stream=True)
    # 写入收到的视频数据
    with open(file_path, 'ab') as file:
        file.write(res.content)
        file.flush()
        # print('receive data，file size : %d   total size:%d' % (os.path.getsize(file_path), content_length))
    print(file_path, '保存完成')


# 读取字幕的m3u8文件
def getSrt(path, name, vttUrl):
    print('开始保存字幕文件')
    url = getVttUrl(vttUrl)
    lists = getVtt(url)
    r = ''
    # 得到精简过后的字符串
    for i in range(0, len(lists)):
        temp = requests.get(lists[i]).text
        temp = temp.replace('WEBVTT', '').strip()
        # 前后均没有换行符，多文件字幕时在中间添加两个换行符
        r = "".join([r, '\n\n', temp])

    # 将.替换为,粗暴替换，字幕中符号影响不大
    r = r.replace('.', ',')

    # 添加序号
    srt_url_list = []
    lines_list = r.strip().split('\n')
    if len(lines_list) < 3:
        lines_list = r.strip().split('\n')

    number = 1
    for index, line in enumerate(lines_list):
        # 使用正则表达式判断加入序号的位置
        pattern = re.compile(r'--\>')
        tem = pattern.findall(lines_list[index])
        # print(index,line)
        if tem:
            srt_url_list.append(str(number))
            number += 1
        srt_url_list.append(lines_list[index])
    srt = '\n'.join(srt_url_list)
    # print(srt)
    # 输出为srt文件
    file_path = path + name + '.srt'
    with open(file_path, 'w') as file:
        file.write(srt)
    print(file_path, '保存完成')
    # print(r)


# 此时获得vtt的url
def getVttUrl(vttUrl):
    r = requests.get(vttUrl).text
    lines_list = r.strip().split('\n')
    if len(lines_list) < 3:
        lines_list = r.strip().split('\n')
    # 获取链接部分
    url = ''
    url2 = ''
    if '#EXTM3U' not in r:
        raise BaseException('非M3U8连接')
    for index, line in enumerate(lines_list):
        # print(index,line)
        # 有的可能没有中文字幕，那就使用英文字母
        if '#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="Chinese"' in line:
            url = lines_list[index]
            url = url[url.find('URI=') + 5:-1]
        if '#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="English"' in line:
            url2 = lines_list[index]
            url2 = url2[url2.find('URI=') + 5:-1]
    # 没有中文字幕的时候使用英文字幕
    if not url:
        url = url2
    return url


def getVtt(m3u8):
    appendUrl = m3u8[:m3u8.rfind('/')+1]
    r = requests.get(m3u8).text.replace('\r', '')
    media_url_list = []
    lines_list = r.strip().split('\n')
    if len(lines_list) < 3:
        lines_list = r.strip().split('\n')

    # 获取链接部分
    if '#EXTM3U' not in r:
        raise BaseException('非M3U8连接')
    for index, line in enumerate(lines_list):
        # print(index,line)
        if '#EXTINF' in line:
            media_url_list.append(appendUrl + lines_list[index + 1])
    # print(media_url_list)
    return media_url_list


def Get():
    url1 = input('输入hbr视频网址:')
    # url1 = 'https://hbr.org/video/5236216251001/what-makes-a-leader'
    pattern = re.compile(r'(?<=/)\d+')

    headers = {
        'Host': 'edge.api.brightcove.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json;pk=BCpkADawqM0_BkIpNQBw-Lbk2C0lOUfgcCL7h0IEpm58jxNabE-P64QU7qsOjNtrPYlco4OmmJfxnyYzdxLQLWXUkfgnAJdn5tFViIaf5fd5nAqtMdLSLO0NeT6i0pBIG4ZtNsdF278WBMJH',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Origin': 'https://hbr.org',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }

    url = 'https://edge.api.brightcove.com/playback/v1/accounts/2071817190001/videos/{}'.format(pattern.findall(url1)[0])
    path = 'E:\\Downloads\\M3U8 1.4.2\\output\\hbr\\'
    html = requests.get(url, headers=headers).text
    jsons = json.loads(html)
    name = jsons['custom_fields']['title']
    videos = jsons['sources']
    # 对列表视频清晰度降序
    videos = sorted(videos, key=lambda videos: videos['width'], reverse=True)
    videoUrl = videos[0]['src']
    # 获得字幕的m3u8地址
    vttUrl = videos[len(videos) - 1]['src']

    # 文件名不能包含\/:*?"<>|
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    name = re.sub(rstr, "_", name)  # 替换为下划线
    getVideo(path, name, videoUrl)
    getSrt(path, name, vttUrl)
# m3u8 = 'https://cdnsecakmi.kaltura.com/p/506471/sp/50647100/playManifest/entryId/1_psw7btzu/format/applehttp/protocol/https/flavorParamIds/457661,457671,457681,457691,457701,457711/video.m3u8?ts=1548948025'
# getSrt('E:\\Downloads\\M3U8 1.4.2\\output\\', 'What Makes a Leader_', m3u8)

Get()
