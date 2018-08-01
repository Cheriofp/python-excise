# -*- coding:utf-8 -*-
import re
import csv
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import pymysql  #(from pymysql import *)

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
        con = pymysql.connect(
            host='localhost', port=3306, database='scrapy',
            user='root', password='lucifer40')
        cur = con.cursor()  # 创建游标对象，对游标对象操作来对数据库进行增删改查
        response = requests.get(url=url, headers=self.headers1).content  # 一级页面回复

        # response = response.decode('GBK').encode('utf-8')
        # with open('response2.txt','w')as res:
        #     res.write(response)

        html = etree.HTML(response)
        title = html.xpath("//div[@class='subject']/a/text()")
        for i in range(len(title)):
            title = html.xpath("//div[@class='subject']/a/text()")[i]
            area = html.xpath("//tr/td[2]/text()")[i].strip()
            huxing = html.xpath("//tr/td[3]/text()")[i].strip()
            price = html.xpath("//tr/td[4]/text()")[i].strip()
            regin = html.xpath("//tr/td[5]/text()")[i].strip()
            link = 'https:'+html.xpath("//div[@class='subject']/a/@href")[i]  # 转至二级页面的链接，还需要加上https:

            # 数据库插入数据的命令
            try:
                cur.execute(
                    '''insert into ningbo19(title,area,huxing,price,regin,link)values(%s,%s,%s,%s,%s,%s);''',(title,area,huxing,price,regin,link,)
                )
                con.commit()
                print('第%s条数据插入成功!'%i)
            except Exception as e:
                print('数据插入失败%s'%e)
            con.rollback()   # 查入失败时数据回滚
            # cur.close()
            # con.close()


    def manage(self):
        start_num = input(u'请输入开始页码：')
        end_num = input(u"请输入结束页码：")
        for page_num in range(int(start_num),int(end_num)+1):
            url = self.url+str(page_num)
            print('正在爬取第%s页数据' % page_num)
            self.spider(url)
        print('数据爬取结束！成功爬取%s页数据'%page_num)
        time.sleep(0.1)

if __name__ == '__main__':
    a = Ning()
    a.manage()
