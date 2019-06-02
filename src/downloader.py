import urllib.request as urq
from urllib.parse import quote
import time
from contextlib import closing
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 伪造headers信息
headers_ = {"Upgrade-Insecure-Requests": '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}


def get_response(url, data=None, headers=None, method=None, decoding="utf-8"):
    """get the response of url"""

    if headers is None:
        headers = headers_
    url = quote(url, safe='/:?=&')
    watch_dog = 0
    response = ''
    while True:
        try:
            request = urq.Request(url, data, headers, method)
            raw_response = urq.urlopen(request)
            if decoding:
                response = raw_response.read().decode(decoding)
            else:
                response = raw_response.read()
        except:  # 发生异常，执行这块代码
            watch_dog += 1
            if watch_dog <= 0:  # 最多尝试3次
                sleep_time = 1.0
                print("第%d次链接失败,%s秒后重试" % (watch_dog, str(sleep_time)))
                time.sleep(sleep_time)
                continue
            else:
                try:
                    print("链接失败!：%s" % url)
                except:
                    print("链接失败!")
                return ''
        else:  # 如果没有异常执行这块代码
            break
    return response


# http://lib.encv/24550.lmg  ==> 24550  or  http://lib.encv/24550  ==> 24550
def get_url_name(url_):
    """从url_中获取名字"""

    raw_res = url_.split('/', -1)[-1]
    raw_res = raw_res.split('.', 1)[0]
    res = raw_res[-15:]
    return res


# http://lib.encv/24550.jpg  ==> jpg  or  http://lib.encv/24550  ==> gif
def get_url_suf(url_, suf_ls=None):
    """从url_中获取后缀"""

    if suf_ls is None:
        suf_ls = [".gif", ".jpg", ".png", ".bmp", ".tif", ".mp4", ".avi"]
    raw_res = url_.split('/', -1)[-1].lower()
    for suf in suf_ls:
        if suf in raw_res:
            return suf
    return suf_ls[0]


# 下载
def supper_download(url, folder_path, pr="", suf="", auto_pr=True, auto_suf=True, headers=None):
    """
    超级下载器，适用于一切文件
    url: 待下载链接
    folder_path: folder path
    auto_pr: 是否使用自动前缀来生成文件名
    auto_suf: 自动后缀
    pr: 前缀
    suf: 后缀
    最终file_name:  auto_pr + pr + suf + auto_suf
    """

    if headers is None:
        headers = headers_
    watch_dog = 0
    while True:
        try:
            with closing(requests.get(url, headers=headers, stream=True, verify=False)) as r:
                chunk_size = 1024 * 10  # 每次写入的块大小
                content_size = int(r.headers['content-length'])

                # 名字生成
                auto_pr = str(content_size) + '+' + get_url_name(url) if auto_pr else ""
                auto_suf = get_url_suf(url) if auto_suf else ""
                copy_tag = ""
                while True:
                    file_name = auto_pr + pr + copy_tag + suf + auto_suf
                    file_path = os.path.join(folder_path, file_name)

                    if os.path.exists(file_path):
                        if os.path.getsize(file_path) == content_size:
                            print('已下载。')
                            return file_path
                        else:
                            copy_tag += "(1)"
                    else:
                        break

                print('%s下载开始！' % suf)
                with open(file_path, 'wb') as f:
                    n = 0
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        n += 1
                        if n % 10 == 0:
                            loaded = 1.0 * n * chunk_size / content_size
                            print('已下载 %s%%' % (str(loaded)))
                    print("%s下载完成！" % suf)
                    return file_path
        except Exception as e:
            watch_dog += 1
            if watch_dog <= 2:  # 最多尝试2次
                sleep_time = 0.3
                print("第%d次链接失败,%s秒后重试" % (watch_dog, str(sleep_time)))
                time.sleep(sleep_time)
                continue
            else:
                print("%s下载失败!" % suf)
                print(Exception, ":", e)
                return ""


if __name__ == "__main__":
    folder = r'E:\pycharm_source\markdown图片管家\test'
    # url__ = "https://image-attachment.oss-cn-beijing.aliyuncs.com/data/www/html/uc_server/data/avatar/001/96/90/89_avatar_middle.jpg?v="\
    url__ = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1559313040830&di=1602a2e80ca8cd3331ff3c66fceb5635&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20181203%2F32b39d8647304af6b3eb6d78c740ea4a.gif"
    print(supper_download(url__, folder))
