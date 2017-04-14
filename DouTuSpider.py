# 斗图网表情包 Spider
# 在原有基础上加上一个多线程：threading 库是 Python 原生多线程处理与控制库

import os
import re
import requests
import threading
from bs4 import BeautifulSoup
from Download import dl


class DouTu:
    def __init__(self):
        self.start_url = 'http://www.doutula.com/'
        os.mkdir('/Users/yton/Documents/斗图')
        os.chdir('/Users/yton/Documents/斗图')

    @staticmethod
    def getImgHref(item):
        img_href_n = item.find('img')
        if img_href_n:
            return {
                'img_name': img_href_n['alt'],
                'img_href': re.findall("this.src='(.*?)'", img_href_n['onerror'])[0]
            }

    def getImgs(self, href, dir_name):
        os.mkdir('/Users/yton/Documents/斗图/' + dir_name)
        os.chdir('/Users/yton/Documents/斗图/' + dir_name)
        soup = BeautifulSoup(dl.GetHtml(href), 'lxml').find_all('div', class_='artile_des')
        img_href_list = [self.getImgHref(item) for item in soup]
        img_href_list.pop()
        self.startSaveImgs(img_href_list)

    def startSaveImgs(self, img_href_list):
        for detail_img in img_href_list:
            img_href = detail_img['img_href']
            img_name = detail_img['img_name']
            # threanding 是多线程处理控制，Thread 是多线程，target 是在线程启动后执行的，args 表示调用 target 的参数列表
            th = threading.Thread(target=self.saveDetailImg, args=(img_name, img_href))
            # 启动线程
            th.start()

    @staticmethod
    def saveDetailImg(img_name, img_href):
        print('[正在抓取]。。。' + img_name + ' ' + img_href)
        # requests.get().text 返回的 Unicode 数据类型，用于获取源码和文本
        # requests.get().content 返回的是二进制数据类型，用于获取文件和图片
        img_content = requests.get(img_href).content
        img_output = open(img_name + '.jpg', 'wb')
        img_output.write(img_content)
        img_output.close()

    def getDetail(self, soup):
        for item in soup:
            href = item['href']
            dir_name = item.find('h4').text
            print('[正在抓取]。。。' + dir_name)
            self.getImgs(href, dir_name)

    def get(self):
        html = dl.GetHtml(self.start_url)
        soup = BeautifulSoup(html, 'lxml')
        max_span = int(soup.find('ul', class_='pagination').find_all('a')[-2].text)
        for page in range(1, max_span + 1):
            href = self.start_url + 'article/list/?page=' + str(page)
            soup = BeautifulSoup(dl.GetHtml(href), 'lxml').find_all('a', class_='list-group-item')
            self.getDetail(soup)


if __name__ == '__main__':
    DouTu().get()
else:
    doutu = DouTu()
