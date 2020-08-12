import requests 
import base64 
import json
#===============================================================#
'''
:使用github 操作 代码存储库，实现增删查改。
'''
user = ''  # 用户名
repo = ''  # 库名
path = ''  # 路径
file_name = ""  # 文件名
token = ""
#===============================================================#


# 将文件转化成base64
def fn_base64(file_name):
    with open(file_name, 'rb') as f:
        fnb64 = base64.b64encode(f.read()).decode('utf-8')
    return fnb64


# 上传新文件
def creat_file(file_name):
    url = "https://api.github.com/repos/{}/{}/contents/{}/{}".format(user, repo, path, file_name)
    d = {
        "message": "my commit message",
        "committer": {
            "name": user,
            "email": "{}@gmail.com".format(user)
        },
        "content": fn_base64(file_name)
    }

    headers = {"Authorization": 'token ' + token}
    r = requests.put(url=url, data=json.dumps(d), headers=headers)
    rs = r.status_code
    if rs == 201:
        print(f'{file_name} upload success')


# 获取已经存在的文件SHA值
def get_sha(file_name):
    headers = {"Authorization": 'token ' + token}
    url = "https://api.github.com/repos/{}/{}/contents/{}/{}".format(user, repo, path, file_name)
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        sha = json.loads(r.text)['sha']
    else:
        sha = ''
    return sha

# 更新文件，也可以上传新文件
def update_file(file_name):
    sha = get_sha(file_name)
    d = {
        "message": "my commit message update",
        "committer": {
            "name": "Scott Chacon",
            "email": "{}@gmail.com".format(user)
        },
        "content": fn_base64(file_name),
        "sha": sha
    }
    url = "https://api.github.com/repos/{}/{}/contents/{}/{}".format(user, repo, path, file_name)
    headers = {"Authorization": 'token ' + token}
    r = requests.put(url=url, data=json.dumps(d), headers=headers)
    r.encoding = "utf-8"
    re_data = json.loads(r.text)
    print(re_data['content']['download_url'])
    print(r.status_code)

# 查找文件
def search_files():
    url = 'https://api.github.com/repos/{}/{}/contents/{}'.format(user, repo, path)
    headers = {"Authorization": 'token ' + token}
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    re_data = json.loads(r.text)
    return re_data

# 删除文件
def del_file(file_name, sha):
    url = "https://api.github.com/repos/{}/{}/contents/{}/{}".format(user, repo, path, file_name)
    d = {
        "message": "delete a file",
        "sha": sha
    }
    headers = {"Authorization": 'token ' + token}
    r = requests.delete(url, headers=headers,data = json.dumps(d))
    r.encoding = "utf-8"
    # re_data = json.loads(r.text)
    if r.status_code == 200:
        print(file_name, ' - 删除成功')

files = search_files()
for file in files:
    file_name = file['name']
    sha = file['sha']
    del_file(file_name, sha)
