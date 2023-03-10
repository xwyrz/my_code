import json
import time

import requests

url = 'https://hhanclub.top/plugin/lucky-draw'
headers = {
    'cookie': '***'
}


def lucky_draw():
    res = requests.post(url=url, headers=headers)
    content = res.text.encode('utf-8').decode('unicode_escape')
    d = json.loads(content)

    # 提取 prize_text 的值
    prize_text = d['data']['prize_text']

    print(f'恭喜你抽中：{prize_text}')


for i in range(30):
    lucky_draw()
    time.sleep(10)
