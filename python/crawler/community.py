# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from conf import cfg
import urllib2
import StringIO
import gzip
import time
import xlwt as excel
import random

# import sys
# 使得 sys.getdefaultencoding() 的值为 'utf-8'  
# reload(sys)  # reload 才能调用 setdefaultencoding 方法  
# sys.setdefaultencoding('utf-8')  # 设置 'utf-8'  

def crawlerjob(url):
    
    try:
        html = getResponseHtml(url)
        
        soup = BeautifulSoup(html)
        list_dist = soup.find(name="li", attrs={'id':'hlist_21'})
        dist = list_dist.findAll(name="a", attrs={'class':''})
        # loop to get district
        for e in dist :
            crawler_shangquan(e.getText(), url, e.get('href'))
            time.sleep(random.randint(1, 10))
            
    except Exception, e:
        print "Exception in crawlerjob ", e
    return None

def crawler_shangquan(district, baseurl, href):
    
    try:
        html = getResponseHtml(url.replace('/housing/', href))
        
        soup = BeautifulSoup(html)
        list_shangquan = soup.find(name="li", attrs={'class':'shangquan'})
        shq = list_shangquan.findAll(name="a", attrs={'class':''})
        # loop to get district
        shequlist = []
        for e in shq :
            shequlist = shequlist + crawler_pages(e.getText(), url.replace('/housing/', e.get('href')))
            time.sleep(random.randint(1, 5))
        
        write_to_excel(district, shequlist)
        
    except Exception, e:
        print "Exception in crawlerjob ", e
    return None

def crawler_pages(district, url):
    # print district, url
    try:
        html = getResponseHtml(url)
        
        soup = BeautifulSoup(html)
        
        totalPages = int(soup.find(name="span", attrs={'class':'fy_text'}).getText().split('/')[1])
#         totalNumber = int(soup.find(name="span", attrs={'class':'number orange'}).getText())
#         totalPages = (totalNumber / 20) if totalNumber % 20 == 0 else (totalNumber / 20 + 1)
#         print str(totalPages)
#         loop pages to get community
        
        shequlist = []
        for pn in range(totalPages) :
            parts = url.split('_')
            parts[-3] = str(pn + 1)
            url = '_'.join(parts)
            print url
            shequlist = shequlist + crawl_page(district, url)
            time.sleep(random.randint(1, 3))
        
        return shequlist
    
    except Exception, e:
        print "Exception in crawler_pages ", e
    return None

def crawl_page(district, url):
    try:
        html = getResponseHtml(url)
        
        soup = BeautifulSoup(html)
        
        houselistdom = soup.find(name="ul", attrs={'id':'houselist'})
        houselist = houselistdom.findAll('dt')
        shequlist = []
        for h in houselist:
            shequlist.append(h.getText().replace('[', ',').replace(']', ',').split(','))
        return shequlist
    
    except Exception, e:
        print "Exception in crawl_page ", e
    return None

def write_to_excel(sheet, datalist):
    fn = 'D:/shequ_' + sheet + '.xls'
    wb = excel.Workbook()
    
    sheet = wb.add_sheet(sheet.decode('utf-8'))
    size = len(datalist)
    for i in range(size):
        for j in range(3):
            try:
                sheet.write(i, j, datalist[i][j])
            except:
                print i, j
    wb.save(fn)
    
def getResponseHtml(url):
    try:
        request = urllib2.Request(url)
        request.add_header('Accept-Encoding', 'gzip')
        response = urllib2.urlopen(request)
        data = response.read()
        response.close()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            data = StringIO.StringIO(data)
            gzipper = gzip.GzipFile(fileobj=data)
            html = gzipper.read()
            gzipper.close()
        else:
            html = data
        html = html.decode('GBK').encode('utf-8')
        return html
    except Exception, e:
        print "No content for ", url, e
    return None

def test():
    for i in range(3):
        print random.randint(1, 5)
    d = '浦东'
    print d.decode('GBK').encode('utf-8')
    print d.decode('utf-8')
        
if __name__ == '__main__':
    url = cfg.getProperty("soufun", "url")
    crawlerjob(url)
#     crawler_pages(u'浦东', 'http://esf.sh.soufun.com/housing/25__0_0_0_0_1_0_0/')
#     test()
    


