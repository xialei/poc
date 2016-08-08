# -*- coding: UTF-8 -*-    或者  #coding=utf-8
import urllib2
import re
from bs4 import BeautifulSoup

def ershoufang():
    # 网站
    suzhou = re.compile('<a name="selectDetail"  gahref="results_click_order_\d" key="su\d{7}" target="_blank" href="/ershoufang/su\d{7}.html" title=.*?>.*?</a>')
    pattern = re.compile(r'\d{7}.html')
    for i in range(1, 101):
        # 网站URL
        urlxx = "http://su.lianjia.com/ershoufang/d" + str(i)
        response = urllib2.urlopen(urlxx)
        html = response.read()
        
        herflink = re.findall(suzhou, html)  # 匹配到想要的连接
        # 遍历跳转链接，抓取数据
        for getlink in herflink:
            # 跳转后URL
            url = "http://su.lianjia.com" + '/ershoufang/su' + pattern.findall(getlink)[0]
            
            print url
            
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read()
            soup = BeautifulSoup(content)
            
            firsttable = soup.find_all('table')[0]

            #房源信息

            titlec = soup.find_all('h1')[0].get_text()             # 标题
            cellc =firsttable.find_all('tr')[4].find_all('td')[0].get_text()                    #小区名称
            addressc =firsttable.find_all('tr')[5].find_all('td')[0].get_text()                  #地址
            unitc =firsttable.find_all('tr')[0].find_all('td')[0].get_text()                   #单价
            totalc=soup.find_all('div', {"class": "price"})[0].get_text()                    #总价
            areac =soup.find_all('div',{"class": "area"})[0].get_text()                   #面积
            layoutc =soup.find_all('div',{"class": "room"})[0].get_text()                 #户型
            floorc =firsttable.find_all('tr')[1].find_all('td')[0].get_text()                    #楼层
            orientationc =firsttable.find_all('tr')[2].find_all('td')[1].get_text()               #朝向
            renovationc =firsttable.find_all('tr')[2].find_all('td')[0].get_text()               #装修情况
            numberc=firsttable.find_all('tr')[6].find_all('td')[0].get_text()                    #编号
            shoufuc=firsttable.find_all('tr')[3].find_all('td')[0].get_text()                    #首付
            monthc=firsttable.find_all('tr')[3].find_all('td')[1].get_text()                    #月供
            
            print titlec, cellc, addressc, unitc, totalc, areac, layoutc, floorc, orientationc, renovationc, numberc, shoufuc, monthc
    
        # http://su.lianjia.com<a name="selectDetail"  gahref="results_click_order_9" key="su1317263" target="_blank" href="/ershoufang/su1317263.html" title="满五唯一少税，实地看房，业主信赖，错过不再有">满五唯一少税，实地看房，业主信赖，错过不再有</a>
        
        break

def winshang():
    url = 'http://biz.winshang.com/html/xm/487/20.htm'
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    div_info = soup.find(name='div', attrs={'class':'xmt'})
    print div_info.findAll(name='li', attrs={'title':'<%=CompanyName%>'})[0].get_text()
        
if __name__ == "__main__":
    winshang()
