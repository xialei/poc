# -*- coding: utf-8 -*- 
import base64
import csv
import datetime
from hashlib import sha1
from hmac import new as hmac
import json
import time
from urllib import urlencode

from django.template.defaultfilters import last
from pandas import Series, DataFrame, concat
from pandas.io.json import json_normalize

import numpy as np
import pandas as pd
import urllib2 as http

import matplotlib as plt


base_url = "http://api.ichinascope.com"

def create_token(access_key, secret_key):
    t = str(time.time())
    token = base64.encodestring(hmac("%s,%s,%s" % (access_key, t, secret_key), digestmod=sha1).digest())[:-1]
    return t, token

def get_security_list(headers):
    params = {"markets":"1001,1002,1003,1012"}
    url = base_url + "/api/stock/list"
    
    req = http.Request(url + "?%s" % urlencode(params), None, headers)
    
    data = http.urlopen(req).read()
    
    if isinstance(data, bytes):
        result = json.loads(data.decode('utf-8'))
    else:
        result = json.loads(data)
    
    return result

def filter_secus(headers):
    
    return   
    
def fetch_hq(headers, secu, rpt_date):
    
    url = base_url + "/api/hq/stock/price/daily"
    end = rpt_date
    start = datetime.datetime.strptime('2016-09-30', "%Y-%m-%d").date() + datetime.timedelta(days=-90)
    params = {"code": secu, "adjusted":'f', "from":start, "to":end}
    req = http.Request(url + "?%s" % urlencode(params), None, headers)
    data = http.urlopen(req).read()
    if isinstance(data, bytes):
        result = json.loads(data.decode('utf-8'))
    else:
        result = json.loads(data)
    
    try:
        stock_data = json_normalize(result['message']).set_index('dt')
    except:
        return 0, 0, 0
    
    stock_hq = stock_data[['tick', 'open', 'close', 'high', 'low', 'vol', 'inc', 'amount', 'turnover']]
    
#     print hq_cross_over(stock_hq)
    
    # first max min last
    return hq_max_min(stock_hq)
    

def hq_max_min(stock_hq):
    
    first = stock_hq.close[0]
    last = stock_hq.close[-1]
    mxdt = stock_hq.close.idxmax()
    mx = stock_hq.close.max()
    mndt = stock_hq.close.idxmin()
    mn = stock_hq.close.min()
    print mxdt, mndt
    sum = stock_hq.inc.sum()
    rr = 0
    dr = 0
    if mndt < mxdt:
        rr = (mx - mn) / mn
        dr = (first - mn) / first
        dr2 = (mx - last) / mx
        if dr2 < dr:
            dr = dr2
    else:
        dr = (mx - mn) / mx
        rr = (mx - first) / first
        rr2 = (last - mn) / mn
        if rr2 > rr:
            rr = rr2
    # print pd.rolling_max(stock_hq.close, len(stock_hq)).dropna().drop_duplicates()
    rr, dr = round(rr * 100, 2), round(dr * 100, 2)
    return rr, dr, sum

def hq_cross_over(stock_hq):
    
    close = stock_hq.close
    
    ma10 = pd.rolling_mean(close, 10)
    ma30 = pd.rolling_mean(close, 30)  # close.rolling(30).mean()
    
    close.plot()
    ma10.plot()
    ma30.plot()
    plt.pyplot.show()
    
    print cross_over(ma10, ma30)

# short term : Series, long term : Series
def cross_over(short, long):
    pre_x = short.shift(1)
    pre_y = long.shift(1)
    up = (pre_x <= pre_y) & (short > long)
    dn = (pre_x >= pre_y) & (short < long)
    up.name = "金叉"
    dn.name = "死叉"
    r = concat([up, dn], axis=1)
    return r[r].dropna(how="all").fillna(0)

def find_top10_shareholders(headers, secus):
    
    holders = {}
    p = "自然人".decode('UTF-8')
    
    t1 = time.time()
    counter = 0
    non_type_holders = []
    for secu in secus:
        counter = counter + 1
#         if counter%5==0:
#             break
        print secu, '\t', str(counter)
        params = {"code" : secu, "count" : 3}
        url = base_url + "/api/stock/trade/holders"
        
        req = http.Request(url + "?%s" % urlencode(params), None, headers)
        
        data = http.urlopen(req).read()
        
        if isinstance(data, unicode):
            result = json.loads(data, encoding='utf-8')
        else:
            result = json.loads(data, encoding='utf-8')
        years_top10 = result['message']
        
        if years_top10 is None:
            print "empty holders : ", secu
        else:
            for y in years_top10.keys():
                
                rr, dr, sum = fetch_hq(headers, secu, y)
                
                top10 = years_top10[y]
                for h in top10:
                    t = h['type']
                    if t is None:
                        print "None holder : ", secu
                        non_type_holders.append(secu)
                    elif t.find(p) >= 0:
                        ph = h['name']
                        shares = h['amount']
                        chr = h['change_ratio']
                        hinfo = {}
                        hinfo['y'] = y
                        hinfo['secu'] = secu
                        hinfo['shares'] = shares
                        hinfo['rr'] = rr
                        hinfo['dr'] = dr
                        hinfo['sum'] = sum
                        if chr is None:
                            hinfo['chr'] = ''
                        else:
                            hinfo['chr'] = chr
                                            
                        if holders.has_key(ph):
                            holders[ph].append(hinfo)
                        else:
                            holders[ph] = [hinfo]
    t2 = time.time()
    print t2 - t1
    dump_result_to_csv(holders)
    if len(non_type_holders) > 0:
        print non_type_holders
    
    
def dump_result_to_csv(holders):
    f = file('D:\holders.csv', 'wb')
    w = csv.writer(f)
    w.writerow(['name', 'num', 'y', 'secu', 'shares', 'change_rate', 'raise max', 'drop min', 'sum of period'])
    for h in holders.keys():
        try:
            hlist = holders[h]
            num = len(hlist)
            for hinfo in hlist:
                w.writerow([h.encode('GBK'), num, hinfo['y'], hinfo['secu'], hinfo['shares'], hinfo['chr'], hinfo['rr'], hinfo['dr'], hinfo['sum']])
        except:
            print h
    f.close()

def testHQ(headers):
    
    fetch_hq(headers, '002552_SZ_EQ', '2016-09-30')
    
def testShareHolders(headers):
    
    result = get_security_list(headers)
  
    seculist = result['message']
    secus = []
    for secu in seculist:
        secus.append(secu['code'])
          
    find_top10_shareholders(headers, secus)
    
if __name__ == '__main__':
    
    access_key = '40ba785900b004d3f70e0a6b8fa0c9ef!'
    secret_key = 'gr+oPgXeerfBGTNiEhWrpCmT8hFrAMXc='
    t, token = create_token(access_key, secret_key)
    print token
    
    headers = {'access_key': access_key, 't':t, 'token':token}
    
#     testShareHolders(headers)
    
    testHQ(headers)
