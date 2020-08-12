#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
下载m3u8格式视频的小组件，使用python3 asyncio
参考了几个大佬的源码 修复了几个小问题。
支持在win系统中使用，包括自动解密，异步请求，设置下载路径，文件名，


"""
import asyncio
import logging
import os
import sys
import time
from asyncio import Queue
from pathlib import Path
from urllib.parse import urljoin
from Crypto.Cipher import AES
import aiohttp
import requests
from tqdm import tqdm

headers = {}
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def m3u8content(m3u8_url):
    logger.debug(f"m3u8_url - {m3u8_url}")
    if m3u8_url.startswith("http"):
        r = requests.get(m3u8_url, timeout=20, headers=headers, verify=True)
        if r.ok:
            ts_list = [urljoin(m3u8_url, n.strip()) for n in r.text.split('\n') if n and not n.startswith("#")]
            if ts_list[0].endswith("m3u8"):
                url = urljoin(m3u8_url, ts_list[0])
                return m3u8content(url)
            return r.text
        else:
            logger.debug(f'response:{r}')
    else:
        return Path(m3u8_url).read_text()

    raise Exception("read m3u8 content error.")



class M3u8Downloader(object):
    def __init__(self, url, path, file_name, worker_num, ts_timeout=120, loop=None, custom_key=None):
        self.file_name = file_name
        self.path = path
        self.url = url
        self.ts_timeout = ts_timeout
        self.cache_dir = path
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)
        self.loop = loop or asyncio.get_event_loop()
        self.ts_list = [urljoin(url, n.strip()) for n in m3u8content(url).split('\n') if n and not n.startswith("#")]
        self.worker_num = worker_num
        self.q = Queue()
        self._ts_name_list = []
        self._fill_q()
        self.ts_length = len(self.ts_list)
        self.download_size = 0


        key = self.read_key() if not custom_key else custom_key

        self.cryptor = None
        if key:
            logger.info(f'key: {key}')
            self.cryptor = AES.new(key, AES.MODE_CBC, key)

    def decode(self, content):
        if self.cryptor:
            return self.cryptor.decrypt(content)
        else:
            return content

    def read_key(self):
        tag_list = [n.strip() for n in m3u8content(self.url).split('\n') if n and n.startswith("#")]
        for s in tag_list:
            if str.upper(s).startswith("#EXT-X-KEY"):
                logger.info(f'{s} found')
                segments = s[len("#EXT-X-KEY") + 1:]
                if segments == "NONE":
                    return None

                logger.info(f'segments:{segments}')
                segments_splited = segments.split(",")
                method = segments_splited[0]
                uri = segments_splited[1]
                method, uri = method.split('=', 1)[1], uri.split('=', 1)[1][1:-1]

                logger.info(f'request uri: {uri}')

                uri = urljoin(self.url, uri)

                r = requests.get(uri, headers=headers)
                if r.status_code == 200:
                    return r.content
                logger.fatal(f"Can`t download key url: {uri}, maybe you should use proxy")
                sys.exit(-1)

    def _fill_q(self):
        for index, ts in enumerate(self.ts_list):
            name = f"{index + 1000}.ts"
            self.q.put_nowait((name, ts))
            self._ts_name_list.append(name)

    async def worker(self):
        async with aiohttp.ClientSession() as session:
            while not self.q.empty():
                name, ts = self.q.get_nowait()
                path = os.path.join(self.cache_dir, name)
                if os.path.exists(path):
                    print("{name} already exists".format(name=name))
                else:
                    try:
                        await self.download(session, path, ts)
                    except Exception as e:
                        print("retry download {name}".format(name=name))
                        logger.warning(e)
                        self.q.put_nowait((name, ts))
                        time.sleep(0.5)
                self.q.task_done()


    async def download(self, session, save_path, url):
        try_count = 5

        logger.debug('[%s] Download %s' % (save_path, url))
        for i in range(try_count):
            if i > 0:
                logger.warning('[%s] Retry to download %s' % (save_path, url))
            try:
                response = await session.get(url)
                content = await response.read()
                file_size = response.headers['Content-Length']
            except Exception as e:
                logger.exception('[%s] Read %s failed: %s' % (save_path, url, e))
                await asyncio.sleep(1)
            else:
                response.raise_for_status()
                break
        else:
            raise RuntimeError('Read %s failed' % url)

        with open(save_path, 'wb') as fp:
            o = self.decode(content)
            fp.write(o)
        self.download_size += file_size
        self.pbar.update(1)


    async def run(self):
        # download all .ts
        logging.info("start download...")
        self.pbar = tqdm(total=self.ts_length, unit='files')
        workers = [asyncio.Task(self.worker(), loop=self.loop) for _ in range(self.worker_num)]
        await self.q.join()
        for w in workers:
            w.cancel()
        self.pbar.close()
        logging.info("download complete , start merge...")
        merge_file(self.cache_dir, self.file_name)


def merge_file(path, file_name):
    os.chdir(path)
    cmd = 'copy /b *.ts "{}".mp4'.format(file_name)
    res = os.popen(cmd)
    if res == 0:
        logging.info('merge .ts to .mp4 complete, start remove .ts ...')
    else:
        logging.warning('出现错误')
    res.close()
    os.system('del /Q *.ts')
    logger.info('remove .ts files complete...')


def main(url, out_path, file_name, worker_num, ts_timeout):
    logging.info(url)
    global headers
    headers["Referer"] = url
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) " \
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    loop = asyncio.get_event_loop()
    downloader = M3u8Downloader(url=url, path=out_path, file_name=file_name, worker_num=worker_num,
                                ts_timeout=ts_timeout, loop=loop)
    loop.run_until_complete(downloader.run())


if __name__ == '__main__':
    m3u8_url = "https://www.123.com/123.m3u8"
    file_name = '****'
    # main(m3u8_url, out_path="E:\\tmp", file_name=file_name, worker_num=10, ts_timeout=120)
    logging.info('All task complete...')
    merge_file(path='E:\\tmp',file_name=file_name)
