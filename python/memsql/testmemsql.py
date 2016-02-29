#!/usr/bin/python
# coding: utf-8
import cymysql
import time
import gevent

def importStockInfo(mysql, memsql):
    cur = mysql.cursor()
    group = "select ticker,org_id,exgh_cd,currency from equity_price_20150116 group by ticker"
    
    mcur = memsql.cursor()
    # ticker, dt, open, close, high, low, inc, vol
    insert = "insert into stock_info values(%s, %s, %s, %s)"
    
    cur.execute(group)
    for r in cur.fetchall():
        # print(r)
        mcur.execute(insert, (r[0], r[1], r[2], r[3]))
    memsql.commit()
    
def importStockQuotes(mysql, memsql):
    cur = mysql.cursor()
    # id, dt, tick, open, close, high, low, inc, vol
    query = "select * from hq_price limit %s,1000"
    mcur = memsql.cursor()
    # ticker, dt, open, close, high, low, inc, vol
    insert = "insert into stock_quotes values(%s, %s, %s, %s, %s, %s, %s, %s)"
    
    for i in range(7000):
        cur.execute(query, (i * 1000 + 1))
        for r in cur.fetchall():
            # print(r)
            mcur.execute(insert, (r[2], str(r[1]), r[3], r[4], r[5], r[6], r[7], int(r[8])))
        memsql.commit()

def testQuery(memsql):
    
    mcur = memsql.cursor();
    
    t1 = time.time()
    sql1 = "select * from stock_quotes where ticker='601398'"
    mcur.execute(sql1)
    t2 = time.time()
    cost1 = t2 - t1  # time in second
    
    sql2 = "select * from stock_quotes where ticker in ('601398', '000983', '600000', '000001')"
    mcur.execute(sql2)
    t3 = time.time()
    cost2 = t3 - t2
    
    # slow query no mater how many times it runs, table scan
    sql3 = "select * from stock_quotes where ticker in (select ticker from stock_info where exgh='SH')"
    mcur.execute(sql3)
    t4 = time.time()
    cost3 = t4 - t3
    
    print cost1, cost2, cost3

def testParallelQuery(memsql):
    
    mcur = memsql.cursor();
    
    t1 = time.time()
    
    sql1 = "select ticker from stock_info where exgh='SH'"
    mcur.execute(sql1)
    
    tickers = []
    
    for r in mcur.fetchall():
        tickers.append(r[0])
        
    part = 64
    sub = len(tickers)/part
    
    print len(tickers), sub
    
    tt = time.time()
    for i in range(part):
        tickerlist = tickers[(i+1)*sub:(i+1)*sub + sub]
        # slow query no mater how many times it runs, table scan
        sql = "select * from stock_quotes where ticker in (%s)"
        tiks = "'" + "','".join(tickerlist) + "'"
        mcur.execute(sql.replace("%s", tiks))
        tt2 = time.time()
        print tt2 - tt
        tt = tt2
    
    t2 = time.time()
    cost = t2 - t1
    print cost
    
if __name__ == "__main__":
    # connect to the Database
    # mysql = cymysql.connect(host='192.168.250.208', user='ada_user', passwd='ada_user', db='ada-fd', charset='utf8')
    memsql = cymysql.connect(host='192.168.0.229', port=3308, user='root', db='stocks', charset='utf8')
    
    # importStockInfo(mysql, memsql)
    # importStockQuotes(mysql, memsql)
#     testQuery(memsql)
    testParallelQuery(memsql)
    
    memsql.close()
    # mysql.close()
    
