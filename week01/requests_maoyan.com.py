#使用requests库获取猫眼 top10
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# 获取猫眼Top10影片详细链接
def getMylist(agent, cookie, url) -> list:
    # 判断请求参数
    if agent == '' or cookie == '' or url == '':
        return []

    header = {
        'user-agent': agent,
        'Cookie': cookie
    }

    response = requests.get(url, headers=header)

    # 判断请求返回码
    if response.status_code != 200:
        return []

    info = bs(response.text, 'html.parser')

    # 创建列表
    List = []
    for tags in info.find_all('div', attrs={'class': 'movie-item film-channel'}):
        href = "https://maoyan.com" + tags.find('a').get('href')
        List.append(href)
        if len(List) > 10:
            break

    return List


def getMyInfo(agent, cookie, url) -> list :

    # 判断请求参数
    if agent == '' or cookie == '' or url == '' :
        return []

    # 设置请求header
    header = {
        'user-agent': agent,
        'Cookie': cookie
    }

    response = requests.get(url, headers=header)

    # 判断请求返回码
    if response.status_code != 200:
        return []

    info = bs(response.text, 'html.parser')

    # 名称
    name = info.find('div',attrs={"class":"movie-brief-container"}).find("h1",attrs={'class':'name'}).text

    # 类型
    lists = info.find_all("li",attrs={"class":"ellipsis"})
    ellipsis = lists[0].text.replace("\n","").strip()
    # 上映日期
    time = info.find_all("li",attrs={"class":"ellipsis"})[2].text

    data = []
    data.append(name)
    data.append(ellipsis)
    data.append(time)
    return data

# 开始抓取
print("start-time:"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
user_agent = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
coookie = '__mta=174397341.1593166132263.1593166146560.1593166258587.3; uuid_n_v=v1; uuid=08940570B79511EAA1F189776DB49E05C2ADF24E320243268AAED2B04040EE34; _csrf=274090bc3afea611b5c6be428852fa61754c55fbfed87b7b8d2dc07e9323d1e3; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593166132; _lxsdk_cuid=172f019f29bc8-0c195289997faa-143f6256-13c680-172f019f29bc8; _lxsdk=08940570B79511EAA1F189776DB49E05C2ADF24E320243268AAED2B04040EE34; mojo-uuid=e4a79b862f7ffbe071a73e14872d964c; mojo-session-id={"id":"dca07b1449c124511dfbb6ba8eb8d187","time":1593172637349}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593172668; __mta=174397341.1593166132263.1593166258587.1593172668394.4; _lxsdk_s=172f07d36b0-c5a-882-9f2%7C%7C4'
myurl = 'https://maoyan.com/films?showType=3'

data = []
list = getMylist(user_agent,coookie,myurl)
for url in list :
    listtemp = getMyInfo(user_agent,coookie,url)
    data.append(listtemp)

movie1 = pd.DataFrame(data = data)
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)
print("end-time:"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))