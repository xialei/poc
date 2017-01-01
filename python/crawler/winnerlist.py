# -*- coding: utf-8 -*-
'''
Created on 2016年12月30日

@author: roger.xia
'''
import httptool
import re
from bs4 import BeautifulSoup
import json
import csv
import random
import time, datetime

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
    
def fetch_winner_list2(dt='2016-12-30'):
    
    print 'start to get ' , dt
    
    url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?tkn=eastmoney&mkt=0&dateNum=&startDateTime=#{dt}&endDateTime=#{dt}&sortRule=1&sortColumn=&pageNum=1&pageSize=200&cfg=lhbggdrtj".replace('#{dt}', dt)
    
    result = httptool.getResponseHtml(url)
    
    '''
    {"Message":"","Status":0,"Data":[{"TableName":"RptLhbXQMap","TotalPage":1,"ConsumeMSecond":0,"SplitSymbol":"|",
    "FieldName":"SCode,SName,ClosePrice,Chgradio,Dchratio,JmMoney,Turnover,Ntransac,Ctypedes,Oldid,Smoney,BMoney,ZeMoney,Tdate,JmRate,ZeRate,Ltsz,Rchange1dc,Rchange1do,
    Rchange2dc,Rchange2do,Rchange3dc,Rchange3do,Rchange5dc,Rchange5do,Rchange10dc,Rchange10do,Rchange15dc,Rchange15do,Rchange20dc,Rchange20do,Rchange30dc,Rchange30do,
    Rchange1m,Rchange3m,Rchange6m,Rchange1y,SumCount,JGBSumCount,JGSSumCount,JGBMoney,JGSMoney,JGJMMoney,DP",
    "Data":["000538|云南白药|76.15|9.9957||9084847.3|161382715|2119274|日涨幅偏离值达到7%的前五只证券|2445780|96344827.7|105429675|201774502.7|2016-12-30|5.63|125.03|79302033544.5|||||||||||||||||||||||||||实力游资买入，成功率72.18%",
    "000612|焦作万方|11.55|8.0449||210253710.31|850814366|75774853|日涨幅偏离值达到7%的前五只证券|2445781|165166791.68|375420501.99|540587293.67|2016-12-30|24.71|63.54|11448045389.55|||||||||||||||||||||||||||买一主买，成功率42.69%",
    "000635|英力特|30.72|-9.9912||-64527768.79|996865377|31485498|日跌幅偏离值达到7%的前五只证券|2445782|110720856.95|46193088.16|156913945.11|2016-12-30|-6.47|15.74|9310851133.44|||||||||||||||||||||||||||实力游资卖出，成功率11.67%"
    '''
    
    result = json.loads(result)
    
    seculist = result['Data'][0]['Data']
    
    lhb = []
    related_securities = []
    
    counter = 0
    for secuinfo in seculist:
        sf = secuinfo.split('|')
        secu = str(sf[0])
        name = sf[1]
        close = sf[2]
        chg = sf[3] # 涨跌幅
        dp = sf[-1]  # 解读
        jm = sf[5]  # 龙虎榜净买额 需要1000
        mr = sf[11]  # 龙虎榜买入额
        mc = sf[10]  # 龙虎榜卖出额
        ze = sf[12]  # 龙虎榜成交额
        turn = sf[6]  # 市场总成交额
        jmrate = sf[14]  # 净买额占总成交比例
        zerate = sf[15]  # 成交额占总成交比
        turn_rate = sf[4]  # 换手率
        ltsz = sf[17]  # 流通市值
        list_reason = sf[8]  # 上榜原因
        
        lhb.append([dt, secu, name.encode('GBK'), close, chg, dp.encode('GBK'), jm, mr, mc, ze, turn, jmrate, zerate, turn_rate, ltsz, list_reason.encode('GBK')])
        
        counter = counter + 1
        buy, sell = fetch_detail(dt, secu, counter)
        related_securities.extend(buy)
        related_securities.extend(sell)
    
    return lhb, related_securities
    
    
def fetch_detail(dt, tik, counter):
    
    url = 'http://data.eastmoney.com/stock/lhb,#dt#,#tik#.html'.replace('#dt#', dt).replace('#tik#', tik)
    
    html = httptool.getResponseHtml(url)
    
    sleeptime = random.randint(1,3)
    time.sleep(sleeptime)
    print dt, tik, sleeptime, counter
    
    if html is None:
        print 'bad response :', dt, tik
        return [], []
    
    soup = BeautifulSoup(html)
    
    buy_tab = soup.find(name="table", attrs={'id':'tab-2'})
    
    sell_tab = soup.find(name="table", attrs={'id':'tab-4'})
    
    buy_rank = parse_table(buy_tab, dt, tik, 'buy')
    
    sell_rank = parse_table(sell_tab, dt, tik, 'sell')
    
    return buy_rank, sell_rank
    
def parse_table(table, dt, tik, flag):
    
    ranklist = []
    
    if table is None:
        return ranklist
    
    buy_tbody = table.findAll(name="tbody")
    
    if buy_tbody is None:
        return ranklist
    
    buy_tr = buy_tbody[0].findAll(name="tr", attrs={'class':''})
    for r in buy_tr:
        try:
            tds = r.findAll("td")
            rank = tds[0].getText()
            security = tds[1].findAll(name="div", attrs={'class':'sc-name'})[0].getText().replace('\n', '').encode('GBK')
            buy = tds[2].getText()
            buy_ratio = tds[3].getText()
            sell = tds[4].getText()
            sell_ratio = tds[5].getText()
            net = tds[6].getText()
            ranklist.append([dt, tik, flag, rank, security, buy, buy_ratio, sell, sell_ratio, net])
        except:
            print 'exception'
    return ranklist

def dump_result_to_csv(fname, headers, datalist):
    f = file(fname, 'wb')
    w = csv.writer(f)
    w.writerow(headers)
    for row in datalist:
        w.writerow(row)
    f.close()

def crawl_winner_list():
    
    end = datetime.datetime.strptime('2016-12-30', "%Y-%m-%d").date()
    days = 2
    result_lhb = []
    result_related_securities = []
    for i in range(days):
        dt = end + datetime.timedelta(days=-i)
        lhb, related_securities = fetch_winner_list2(str(dt))
        result_lhb.extend(lhb)
        result_related_securities.extend(related_securities)
    dump_result_to_csv('./lhb.csv', ['dt', 'secu', 'name', 'close', 'chg', 'dp', 'jm', 'mr', 'mc', 'ze', 'turn', 'jmrate', 'zerate', 'turn_rate', 'ltsz', 'list_reason'], result_lhb)
    dump_result_to_csv('./lhb_related_secus.csv', ['dt', 'tik', 'flag', 'rank', 'security', 'buy', 'buy_ratio', 'sell', 'sell_ratio, net'], result_related_securities)
    
if __name__ == '__main__':
    crawl_winner_list()
    pass
