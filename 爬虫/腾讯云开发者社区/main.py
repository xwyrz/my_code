import requests
import json
import time

url = 'https://cloud.tencent.com/developer/api/home/article-list'

for i in range(229):
  dic = {"pageNumber":i+1,"type":"recommend"}
  string = json.dumps(dic)
  headers = {"Content-Type": "application/json; charset=UTF-8;"}
  r = requests.post(url, data=string, headers=headers)
  res = json.loads(r.text)
  # print(res["data"]["list"])
  for value in res["data"]["list"]:
    article_id = value["articleId"]
    article_url = f"https://cloud.tencent.com/developer/article/{article_id}"
    with open(file="url.txt",mode="a",encoding="utf-8") as f:
      f.write(article_url+'\n')
  print(f'当前请求页数：{i+1}')
  time.sleep(2)
