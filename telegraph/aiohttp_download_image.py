import logging
import os
import re
import ssl
import time

import aiohttp, asyncio
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

# 获取所有图片链接地址
def get_img_links(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('title')
        title = str(title)[7:-20]
        # 去除标题中的特殊符号
        title = re.sub('[\/:*?"<>|]', '-', title)
        url_list = []
        images = soup.findAll("img")
        for img in images:
            url_list.append('https://telegra.ph' + img['src'])
        return (title, url_list)
    else:
        logging.error('请求失败，状态码为%s' % response.status_code)


async def main(pool, url, path):  # 启动
    sem = asyncio.Semaphore(pool)
    worker = get_img_links(url)
    dirname = worker[0]
    links = worker[1]
    file_path = os.path.join(path, dirname)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    async with aiohttp.ClientSession() as session:  # 给所有的请求，创建同一个session
        tasks = []
        [tasks.append(control_sem(sem, url, session, file_path)) for url in links]
        tasks_iter = asyncio.as_completed(tasks)
        # 创建一个进度条
        fk_task_iter = tqdm(tasks_iter, total=len(links), unit='files')
        for coroutine in fk_task_iter:
            # 获取结果
            await coroutine


async def control_sem(sem, url, session, path):  # 限制信号量
    async with sem:
        await fetch(url, session, path)


async def fetch(url, session, path):  # 开启异步请求
    src_name = url.split('/')[-1]
    async with session.get(url, timeout=60) as resp:  # 设置超时
        with open(os.path.join(path, src_name), 'wb') as fd:
            while True:
                chunk = await resp.content.read(1024)  # 每次获取1024字节
                if not chunk:
                    break
                fd.write(chunk)


url = ''
path = "E:\\ChromeDownloads\\图片助手(ImageAssistant) 批量图片下载器"
pool_num = 5
start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(pool=pool_num, url=url, path=path))
end = time.time()
logging.info(f'总下载耗时:{end - start}')
