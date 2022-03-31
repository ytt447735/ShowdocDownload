import os
import time
import re
import requests
import ujson
from urllib.parse import urlparse

url = input("请输入showdoc文档链接：")
if url == None or url == "":
    os.system("pause")
#url = "https://www.showdoc.com.cn/WxApiUltimatePublicNew/3101328044405668"
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)


def GetPage(page_id):
    url = "https://www.showdoc.cc/server/index.php?s=/api/page/info"
    data = {
        "page_id": page_id,
        "_item_pwd": "null"
    }
    res = requests.post(url=url, data=data)
    j = ujson.loads(res.text)
    c = j["data"]["page_content"]
    s = re.findall(r'!\[\]\((.*?)\)', c)
    for a in s:
        f = DownImg(a)
        if f != "":
            c = str(c).replace("![](" + a + ")", "![](" + f + ")")
        time.sleep(0.2)
    return c


def Handle(t):
    return str(t).replace(" ", "").replace(" ", "").replace("(", "【").replace(")", "】").replace("[", "【").replace("]", "】")


def DownImg(url):
    r = requests.get(url)
    p = ["bmp", "jpg", "png", "tif", "gif", "pcx", "tga", "exif", "fpx", "svg", "psd", "cdr", "pcd", "dxf", "ufo",
         "eps", "ai", "raw", "WMF", "webp", "avif", "apng", "jpeg"]
    pathname = ""
    for n in p:
        if n in str(r.headers.get('Content-Type')).lower():
            try:
                path = r.headers.get("Content-Disposition")
                path = re.findall(r'filename="(.*?)"', path)
                pathname = "img/" + path[0]
                path = os.path.join(BasicPath, "img", path[0])
                open(path, 'wb').write(r.content)
            except:
                path = os.path.basename(url)
                path = path.replace("\\", "").replace("/", "").replace(":", "").replace("*", "").replace("?",
                                                                                                         "").replace(
                    "\"", "").replace("<", "").replace(">", "").replace("|", "")
                pathname = "img/" + path
                path = os.path.join(BasicPath, "img", path)
                open(path, 'wb').write(r.content)
            break
    return pathname

p = urlparse(url)
c = p.path.split('/')
url = "https://www.showdoc.cc/server/index.php?s=/api/item/info"
data = {
    "item_id": c[1],
    "keyword": "",
    "default_page_id": c[2],
    "_item_pwd": "null"
}
res = requests.post(url=url, data=data)
j = ujson.loads(res.text)
p = j["data"]["item_name"]
if not os.path.exists(os.path.join(dir_name, p)):
    os.mkdir(os.path.join(dir_name, p))
BasicPath = os.path.join(dir_name, p)
if not os.path.exists(os.path.join(BasicPath, "img")):
    os.mkdir(os.path.join(BasicPath, "img"))
menu = ""
page = ""
menu = menu + "<!-- GFM-TOC -->" + "\r\n"
for m in j["data"]["menu"]["pages"]:
    name = Handle(m["page_title"])
    menu = menu + "* [{0}](#{0})".format(name) + "\r\n"
    name = Handle(m["page_title"])
    page = page + "#{0}".format(name) + "\r\n"
    page = page + GetPage(m["page_id"]) + "\r\n"
    time.sleep(0.2)

for m in j["data"]["menu"]["catalogs"]:
    name = Handle(m["cat_name"])
    menu = menu + "* [{0}](#{0})".format(name) + "\r\n"
    index = 0
    for pa in m["pages"]:
        print(pa["page_title"], pa["page_id"])
        index = index + 1
        if index == 1:
            name = Handle(m["cat_name"])
            page = page + "#{0}".format(name) + "\r\n"
        name = Handle(pa["page_title"])
        menu = menu + "  * [{0}](#{0})".format(name) + "\r\n"
        page = page + "##{0}".format(name) + "\r\n"
        page = page + GetPage(pa["page_id"]) + "\r\n"
        time.sleep(0.1)
    time.sleep(0.2)
menu = menu + "<!-- GFM-TOC -->" + "\r\n"
file_object = open(os.path.join(p, "index.md"), 'w', encoding='utf-8')
file_object.write(menu + page)
file_object.close()
os.system("pause")
'''
def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
'''