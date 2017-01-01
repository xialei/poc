# -*- coding: utf-8 -*-
'''
Created on 2016年12月30日

@author: roger.xia
'''
import httptool
import re
from bs4 import BeautifulSoup
import json

def fetch_winner_list():
    
    dt = '2016-12-30'
    url = 'http://data.eastmoney.com/stock/tradedetail/#dt#.html'.replace('#dt#', dt)
    
    html = httptool.getResponseHtml(url)
    
    data_re = re.compile('var data_tab_1=(.*?);')
    
    # default_tab = soup.findAll(data_re)
    default_tab = data_re.findall(html)
    
    result = json.loads(unicode(default_tab[0], 'GBK'))
    
    # {u'Rchange1do': u'', u'Chgradio': u'9.9957', u'Rchange3m': u'9.99566662', u'Rchange10do': u'', u'Rchange1dc': u'', 
    # u'JD': u'\u5b9e\u529b\u6e38\u8d44\u4e70\u5165\uff0c\u6210\u529f\u738772.18%', u'Rchange20dc': u'', u'Rchange10dc': u'', u'Rchange5do': u'', 
    # u'ZeRate': u'125.03', u'Rchange20do': u'', u'Rchange1y': u'3.41536031', u'Rchange5dc': u'', u'JGSMoney': u'', u'JmMoney': u'9084847.3', 
    # u'Ctypedes': u'\u65e5\u6da8\u5e45\u504f\u79bb\u503c\u8fbe\u52307%\u7684\u524d\u4e94\u53ea\u8bc1\u5238', u'Rchange2do': u'', 
    # u'JGBMoney': u'', u'Rchange3do': u'', u'Rchange30do': u'', u'Ntransac': u'2119274', u'Oldid': u'2445780', u'Rchange15dc': u'', u'Rchange15do': u'', 
    # u'Turnover': u'161382715', u'Rchange3dc': u'', u'Rchange2dc': u'', u'JmRate': u'5.63', u'ClosePrice': u'76.15', u'SName': u'\u4e91\u5357\u767d\u836f', 
    # u'Rchange6m': u'18.68765586', u'Tdate': u'2016-12-30', u'Rchange1m': u'9.99566662', u'SCode': u'000538', u'Smoney': u'96344827.7', u'Bmoney': u'105429675', 
    # u'ZeMoney': u'201774502.7', u'Dchratio': u'0.204', u'JGSSumCount': u'', u'DP': u'\u5b9e\u529b\u6e38\u8d44\u4e70\u5165\uff0c\u6210\u529f\u738772.18%', 
    # u'JGBSumCount': u'', u'SumCount': u'', u'Ltsz': u'79302033544.5', u'Rchange30dc': u'', u'JGJMMoney': u''}
    for tik in result['data']:
        secu = tik['SCode']
        name = tik['SName']
        close = tik['ClosePrice']
        chg = tik['Chgradio']
        dp = tik['DP']  # 解读
        jm = tik['JmMoney']  # 龙虎榜净买额 需要1000
        mr = tik['Bmoney']  # 龙虎榜买入额
        mc = tik['Smoney']  # 龙虎榜卖出额
        ze = tik['ZeMoney']  # 龙虎榜成交额
        turn = tik['Turnover']  # 市场总成交额
        jmrate = tik['JmRate']  # 净买额占总成交比例
        zerate = tik['ZeRate']  # 成交额占总成交比
        turn_rate = tik['Dchratio']  # 换手率
        ltsz = tik['Ltsz']  # 流通市值
        list_reason = tik['Ctypedes']  # 上榜原因
        
        fetch_detail(dt, secu)
        print secu, name, close, chg, dp, jm, mr, mc, ze, turn, jmrate, zerate, turn_rate, ltsz, list_reason
        break

def fetch_detail(dt, tik):
    
    url = 'http://data.eastmoney.com/stock/lhb,#dt#,#tik#.html'.replace('#dt#', dt).replace('#tik#', tik)
    
    html = httptool.getResponseHtml(url)
    
    soup = BeautifulSoup(html)
    
    buy_tab = soup.find(name="table", attrs={'id':'tab-2'})
    
    sell_tab = soup.find(name="table", attrs={'id':'tab-4'})
    
    print buy_tab, sell_tab

if __name__ == '__main__':
    fetch_winner_list()
    pass
