# 斗图网表情包 Spider

import os, re, requests
from Download import dl
from bs4 import BeautifulSoup


class DouTu:
    def __init__(self):
        self.start_url = 'http://www.doutula.com/'

    def storeImgs(self, href, dir_name):
        os.mkdir(dir_name)
        soup = BeautifulSoup(dl.GetHtml(href), 'lxml').find_all('div', class_='artile_des')
        for item in soup:
            img_href_n = item.find('img')
            if img_href_n:
                img_name = img_href_n['alt']
                img_href = re.findall("this.src='(.*?)'", img_href_n['onerror'])[0]
                print('[正在抓取]。。。' + img_name + ' ' + img_href)
                # requests.get().text 返回的 Unicode 数据类型，用于获取源码和文本
                # requests.get().content 返回的是二进制数据类型，用于获取文件和图片
                img_content = requests.get(img_href).content
                img_output = open(dir_name + os.sep + img_name + '.jpg', 'ab')
                img_output.write(img_content)
                img_output.close()

    def getDetail(self, soup):
        for item in soup:
            href = item['href']
            dir_name = item.find('h4').text
            print('[正在抓取]。。。' + dir_name)
            self.storeImgs(href, dir_name)

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
