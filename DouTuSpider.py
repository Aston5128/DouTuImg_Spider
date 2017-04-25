# 抓取斗图网的表情包
# 在原有基础上加上一个多线程：threading 库是 Python 原生多线程处理与控制库
# 亲测抓取一个页面完整的所有图片需要 2 秒左右，比未添加超线程的满了5倍，提速明显
# 继续改进，使用 lxml 的 etree 代替 BeautifulSoup 进一步提升速度

import os
import requests
import threading
from lxml import etree
from Download import dl


def get():
    """创建主文件夹，开始爬取"""
    os.mkdir('/Users/yton/Documents/斗图')
    os.chdir('/Users/yton/Documents/斗图')
    html = etree.HTML(dl.GetHtml('https://www.doutula.com/'))  # 用 etree 分析 index
    max_span = int(html.xpath('//li')[16].xpath('string(.)'))  # 获取最大页的页码
    for page in range(1, max_span+1):
        url = 'https://www.doutula.com/article/list/?page=' + str(page)
        print('[正在抓取]。。。url: ' + url)
        html = etree.HTML(dl.GetHtml(url))
        getDetail(html)

def getDetail(html):
    """获取子页面的数据"""
    href_list = [str(item.xpath('@href')[0]) for item in html.xpath('//a[@class="list-group-item"]')]
    for url in href_list:
        html = etree.HTML(dl.GetHtml(url))
        dir_name = str(html.xpath('//li[@class="list-group-item"]//h3//blockquote//a')[0].xpath('string(.)'))
        print('[正在抓取]。。。' + dir_name)
        if os.path.exists('/Users/yton/Documents/斗图/' + dir_name): pass
        else:
            os.mkdir('/Users/yton/Documents/斗图/' + dir_name)
            os.chdir('/Users/yton/Documents/斗图/' + dir_name)
        getImgs(html)

def getImgs(html):
    """获取图片的名字和"""
    img_n = html.xpath('//div[@class="artile_des"]//table//a//img')
    img_dict_list = [{'img_name': str(item.xpath('@alt')[0]), 'img_href': str(item.xpath('@src')[0])} for item in img_n]
    for img_dict in img_dict_list:
        threading.Thread(target=storeImg, args=(img_dict, )).start()  # 多线程

def storeImg(img_dict):
    """保存图片"""
    print('[正在抓取]。。。' + img_dict['img_name'])
    with open(img_dict['img_name'] + '.jpg', 'wb') as p:
        p.write(requests.get('http:' + img_dict['img_href']).content)

if __name__ == '__main__':
    get()
