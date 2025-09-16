import requests
import csv
from lxml import etree
import time


'''

本程序可获取芜湖市建设工程造价管理站发布的工程材料信息价
1. http://xxj.gldjc.com/search/toSearch
2. cookies可能会改变
3. 每期对应formdata内的searchid如下：
  日期    searchid 
2018-07:   5328
2018-06:   5276
2018-05：  5212
2018-04：  5157
2018-03：  5081
2018-02：  4962
2018-01：  4919
2017-12：  4883
2017-11：  4804

'''

searchid = []
id_issue = {5328:'2018年07期',5276:'2018年06期',5212:'2018年05期',5157:'2018年04期',5081:'2018年03期',
            4962:'2018年02期',4919:'2018年01期',4883:'2017年12期',4804:'2017年11期'}

def parse_item(searchid):
    page = 1
    isend = False
    url = 'http://xxj.gldjc.com/search/ajax/searchList'
    reqheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Cookie': 'gldjc_sessionid=99d80521-e545-414e-8fc2-3c47d5b2ff80',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                 }
    

    while isend == False:
        
        formdata = {'currentPage': page,
                    'searchId': searchid,
                   }
        time.sleep(0.5)
        r = requests.post(url,headers=reqheaders,data=formdata)
        pagex = etree.HTML(r.text)
        if not pagex.xpath("//tbody/tr/td/div/text()"):
            isend = True
        print('抓取期数： %s ,页数：%d' % (id_issue[searchid],page))
        for each in pagex.xpath("//tbody/tr"):
            item = []

            if each.xpath("./td/div/text()"):
                codeid = each.xpath("./td/div/text()")
            else:
                codeid = ['-']

            if each.xpath("./td[2]/text()"):
                name = each.xpath("./td[2]/text()")
            else:
                name = ['-']

            if each.xpath("./td[3]/text()"):
                model = each.xpath("./td[3]/text()")
            else:
                model = ['-']

            if each.xpath("./td[4]/text()"):
                units = each.xpath("./td[4]/text()")
            else:
                units = ['-']

            if each.xpath("./td[5]/text()"):
                price_tax = each.xpath("./td[5]/text()")
            else:
                price_tax = ['-']

            if each.xpath("./td[6]/text()"):
                price_notax = each.xpath("./td[6]/text()")
            else:
                price_notax = ['-']

            if each.xpath("./td[9]/text()"):
                date = each.xpath("./td[9]/text()")
            else:
                date = ['-']

            infodate = id_issue[searchid]
            infodate = [infodate]

            item = codeid + name + model + units + price_tax + price_notax + date + infodate
            with open('wuhump.csv', 'a') as csvfile:
                writer = csv.writer(csvfile,lineterminator='\n')
                writer.writerow(item)
            
            
        page += 1
    # csvfile.close()

# 第一次运行时开启以下代码段
# with open('wuhump.csv', 'a') as csvfile:
#     writer = csv.writer(csvfile,lineterminator='\n')
#     writer.writerow(['编码','名称','规格型号','单位','含税价格(元)','除税价格(元)','发布日期','期数'])
# csvfile.close()

for id in searchid:
    parse_item(id)