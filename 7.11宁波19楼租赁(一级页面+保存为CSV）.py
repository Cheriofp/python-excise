# -*- coding:utf-8 -*-
import re
import csv
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from multiprocessing import Pool

class Ning:
    def __init__(self):
        self.url = 'https://ningbo.19lou.com/thread/category/structure/search/result?fid=1996&m=10060&page='
        self.headers1 = {
            'Host': 'ningbo.19lou.com',
            # 'Referer': 'https://ningbo.19lou.com/forum-1996-1.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

    def spider(self,url):
        response = requests.get(url=url, headers=self.headers1).content  # 一级页面回复

        # response = response.decode('GBK').encode('utf-8')
        # with open('response2.txt','w')as res:
        #     res.write(response)

        html = etree.HTML(response)
        title = html.xpath("//div[@class='subject']/a/text()")
        area = html.xpath("//tr/td[2]/text()")
        huxing = html.xpath("//tr/td[3]/text()")
        price = html.xpath("//tr/td[4]/text()")
        regin = html.xpath("//tr/td[5]/text()")
        links = html.xpath("//div[@class='subject']/a/@href")  # 转至二级页面的链接，还需要加上https:
        with open('宁波19楼result.csv', 'a')as f:
            writer = csv.writer(f)
            # writer.writerow(['标题', '地区', '户型', '价格', '来源', '链接'])
            for i in range(0, len(title)):
                writer.writerow(
                    [title[i].strip(), area[i].strip(), huxing[i].strip(), price[i].strip(), regin[i].strip(),
                     "http:" + links[i]])

                # print('正在写入第%s行数据' %i)

    def manage(self):
        start_num = input(u'请输入开始页码：')
        end_num = input(u"请输入结束页码：")
        for page_num in range(int(start_num),int(end_num)+1):
            url = self.url+str(page_num)
            print('正在爬取第%s页数据' % page_num)
            self.spider(url)
        print('数据爬取结束！成功爬取%s页数据'%page_num)
            # time.sleep(0.1)

if __name__ == '__main__':

    a = Ning()
    a.manage()

    pool = Pool(processes=3)
    pool.map()

