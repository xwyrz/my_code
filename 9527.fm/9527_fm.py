'''
:爬取9527.fm网站播放源的爬虫，并将结果保存到Google sheet！
'''
from __future__ import print_function
from oauth2client import file, client, tools
from googleapiclient.discovery import build
import logging
import ssl
import requests
from lxml import etree

# 屏蔽warning信息
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

logging.getLogger('googleapicliet.discovery_cache').setLevel("WARNING")
SCOPES = 'https://www.googleapis.com/auth/drive'  # 设置Google权限API范围

store = file.Storage('token.json')
creds = store.get()
flags = tools.argparser.parse_args(args=[])
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags)
sheet_service = build('sheets', 'v4', credentials=creds)
sheet_id = '1ggThOJ7dq6CrWOsdch5FFT_iUVqVfMpC1O3JX0vnLDw'  # sheet表格ID
sheet_name = 'tv'
range_name = ('{}!A2:K'.format(sheet_name))


def set_values(values):
    set_values = [values]
    body = {'values': set_values, 'majorDimension': 'ROWS'}
    sheet_service.spreadsheets().values().append(spreadsheetId=sheet_id,
                                                 range=range_name,
                                                 valueInputOption="RAW",
                                                 insertDataOption="INSERT_ROWS",
                                                 body=body).execute()


def my_requests(url):
    try:
        response = requests.get(url, verify=False)
    except:
        print("网络请求异常，正在重试！")
        response = requests.get(url, verify=False)
    response.encoding = 'gb2312'
    selector = etree.HTML(response.text)
    return selector


def get_info(url, num):
    print('开始处理网页：', url)
    host = 'https://www.9527.fm'
    html_sel = my_requests(url)
    # 标题
    title = html_sel.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li[1]/h1/text()')[0]
    # 封面
    logo = html_sel.xpath('/html/body/div[3]/div/div[1]/div[1]/img/@src')[0]
    # 更新状态
    status = html_sel.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li[2]/text()')[0]
    # 又名
    sub_name = html_sel.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li[3]/text()')[0]
    # 标签
    tags = html_sel.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li[4]/a/text()')
    tag = ",".join(tags)
    # 时间
    movie_times = html_sel.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li[5]/text()')
    movie_time = ",".join(movie_times)
    # 豆瓣评分
    douban_num = html_sel.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li[6]/span[2]/text()')[0]
    # 导演，演员
    authors = html_sel.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li[7]/a/text()')
    author = ",".join(authors)
    # 简介
    movie_info = html_sel.xpath('//*[@id="fullContent"]/text()')[0]
    values = []

    # 判断是否有播放源
    movie_plays = html_sel.xpath('/html/body/div[3]/div/div[4]/div[1]/div/div')
    if len(movie_plays) != 0:
        urls = ""
        for i in range(len(movie_plays)):
            movie_play_html = html_sel.xpath('/html/body/div[3]/div/div[4]/div[1]/div/div[{}]/ul/li/a/@href'.format(i))
            movie_play_name = html_sel.xpath('/html/body/div[3]/div/div[4]/div[1]/div/div[{}]/ul/li/a/text()'.format(i))
            movie_urls = ""
            for a in range(len(movie_play_html)):
                m3u_name = movie_play_name[a]
                m3u_html = host + movie_play_html[a]
                m3u_sel = my_requests(m3u_html)
                m3u_url = m3u_sel.xpath('//*/div/video/source/@src')[0]
                m3u_play_url = '{}#{}'.format(m3u_name, m3u_url)
                movie_urls += '{}&'.format(m3u_play_url)
            urls += '{}$'.format(movie_urls)
    else:
        urls = ""
        print('当前页面无播放地址！')
    values.append(num)
    values.append(title)
    values.append(logo)
    values.append(status)
    values.append(sub_name)
    values.append(tag)
    values.append(movie_time)
    values.append(douban_num)
    values.append(author)
    values.append(movie_info)
    values.append(urls)
    set_values(values)

for i in range(1, 26041):
  url = 'https://www.9527.fm/tv/{}.html'.format(i)
  get_info(url, num=i)
