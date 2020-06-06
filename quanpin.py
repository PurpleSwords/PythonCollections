import time
import requests
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getVideoUrl(url):
    browser = webdriver.PhantomJS(executable_path=r'E:\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    #url = 'https://wk.canpoint.net/video/v/6s5D25wtTnAcjC4UiPklWQ==.html'
    browser.get(url)

    #超时判断
    element = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//video[@src]")))

    html = browser.page_source
    select = etree.HTML(html)
    video = select.xpath('//video/@src')[0]
    title = select.xpath('//p[@class="top_title"]/b/text()')[0]
    print(video, title)
    return video, title


def getVideo(path, url, title):
    print('开始下载视频文件{},{}'.format(title, url))
    file_path = path + title + '.mp4'
    recvlen = 0
    r = requests.get(url, stream=True)
    # 写入收到的视频数据
    with open(file_path, 'ab') as file:
        # 限速用
        for chunk in r.iter_content(chunk_size=30720*5):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)
                recvlen = recvlen + len(chunk)
                time.sleep(0.1)
                file.flush()

        #file.write(r.content)
        #file.flush()
        #print('receive data，file size : %d   total size:%d' % (os.path.getsize(file_path), content_length))
    print(file_path, '保存完成')


def getUrl():
    ListUrl = []
    for i in range(1, 45):
        url = 'https://ms.canpoint.net/Teacher/View/teaching.html?p={}&tid=6s5D25wtTnDCZayyHCI7xw%3D%3D'.format(i)
        html = setRequest(url).text
        select = etree.HTML(html)
        htmlUrl = select.xpath('//p[@class="p_title"]/a/@href')
        ListUrl.extend(htmlUrl)
        print('已获取{}/44页课程内容'.format(i))
    #print('-----------------------------')
    #print(ListUrl)
    #print(len(ListUrl))
    time.sleep(10)
    return ListUrl


# 解决网络出错问题，进行重试
def setRequest(url, headers='', sleep=60, number=10):
    # 下载超时的处理方式：
    for i in range(0, number):
        try:
            if headers == '':
                key = requests.get(url)
            else:
                key = requests.get(url, headers=headers)
            break
        except:
            print('休息{}s，进行第{}次重试'.format(sleep, i+1))
            time.sleep(60)
    if i == number:
        print(url, '重试{}次失败'.format(i))
    return key


def main():
    listUrl = getUrl()
    lenght=len(listUrl)
    for i in range(0, lenght):
        videoUrl, title = getVideoUrl(listUrl[i])
        path = 'E:\\demo\\初中物理\\'
        getVideo(path, videoUrl, title)
        print('第{}个视频下载完成:{} {}'.format(i+1, title, videoUrl))
        print('休息60s')
        time.sleep(60)
    print('下载完成')


if __name__ == '__main__':
    # video, title=getVideoUrl('https://wk.canpoint.net/video/v/6s5D25wtTnAcjC4UiPklWQ==.html')
    # getVideo('E:\\demo\\初中物理\\', video, 'test')
    main()
