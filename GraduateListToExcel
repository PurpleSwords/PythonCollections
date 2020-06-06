import requests
from lxml import etree
import pandas as pd
import time


def creatExcel():
    df = pd.DataFrame({'题目问题': [], '学院': [], '时间': [], '具体问题': [], '具体解答': []})
    df.to_excel('getData.xlsx', encoding='utf-8')
    return df


def getList(df):
    headers = {
        # 'accept': 'application/json, text/plain, */*',
        # 'accept-encoding': 'gzip, deflate, br',
        #'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'cookie': '__utmz=66713403.1572491578.20.2.utmcsr=wiki.arcaea.cn|utmccn=(referral)|utmcmd=referral|utmcct=/index.php/%E6%90%AD%E6%A1%A3; __utmc=66713403; __utma=66713403.817354715.1571657084.1579614538.1579616756.115',
        #'dnt': '1',
        # 'referer': 'https://diverse.direct/',
        #'sec-fetch-mode': 'cors',
        #'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    start = 0
    end = 645
    for start in range(0, end+1, 15):
        url = 'https://yz.chsi.com.cn/zxdy/forum--method-listDefault,year-2020,forumid-450335,start-{}.dhtml'.format(start)
        html = setRequest(url, headers).text
        select = etree.HTML(html)

        i = 0
        number = len(select.xpath('//table/tr'))
        # print(number)
        while True:
            i += 1
            question = select.xpath('//table/tr[{}]/td[2]/a/text()'.format(i))[0].strip()

            # print(question)
            collage = select.xpath('//table/tr[{}]/td[3]/div/text()'.format(i))[0].strip()
            times = select.xpath('//table/tr[{}]/td[5]/text()'.format(i))[0].strip()
            i += 1
            questions = select.xpath('//table/tr[{}]/td[2]/div/div[1]'.format(i))[0].xpath('normalize-space(string(.))').strip()
            answers = select.xpath('//table/tr[{}]/td[2]/div/div[2]'.format(i))[0].xpath('normalize-space(string(.))').strip()
            # print(html)
            print(question, collage, times)
            print(questions, answers)
            # 直接插入数据
            new = pd.DataFrame({'题目问题': [question], '学院': [collage], '时间': [times], '具体问题': [questions], '具体解答': [answers]})
            # 忽略原来的索引，从0开始自增
            df = df.append(new, ignore_index=True)
            # 结束循环
            if i == number:
                break
        df.to_excel('getData.xlsx', encoding='utf-8')
        time.sleep(2)


# 解决网络出错问题，进行重试
def setRequest(url, headers='', sleep=60, number=5):
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
            time.sleep(sleep)
    if i == number:
        print(url, '重试{}次失败'.format(i))
    return key


if __name__ == '__main__':
    df = creatExcel()
    getList(df)
