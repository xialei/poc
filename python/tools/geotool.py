# -*- coding: utf-8 -*-
'''
Created on 2014年4月3日

@author: Roger.xia
'''
from conf import cfg
import urllib2
import json
import time
import random

def getGeoLocation():
    url = cfg.getProperty("baiduapi", "geo_url")
    fout = open("D:/shequloc.txt", "a")
    with open('D:/shequ.txt', 'r') as f:
        loop = 0
        for line in f:
            addr = line.rstrip()
            lng, lat = geoinfo(url, addr)
            print lng, lat
            fout.write(addr + ',' + lng + ',' + lat + '\n')
            loop = loop + 1
            if loop % 20 == 0 :
                fout.flush()
                time.sleep(random.randint(2, 5))
    fout.close()

def geoinfo(url, address):
    url = url.replace('#{address}', address)
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        res = json.load(response)
        key = 'result'
        if 'results' in res:
            key = 'results'
        result = res[key]
        if not len(result):
            return '', ''
        loc = result["location"]
        response.close()
        return str(loc["lng"]), str(loc["lat"])
    except Exception, e:
        print "exception in geoinfo: ", url, e
        return '', ''

def test():
    res = 'showLocation&&showLocation({"status":0,"result":{"location":{"lng":121.55659515381,"lat":31.205045949614},"precise":1,"confidence":70,"level":"\u5730\u4ea7\u5c0f\u533a"}})'
    res = res[27:][0:-1]
#     res = '{"results":[],"status":1,"msg":"Internal Service Error:\u65e0\u76f8\u5173\u7ed3\u679c"}'
    if 'results' in res:
        key = 'results'
    else:
        key = 'result'
    result = json.loads(res)[key]
    if not len(result):
        return
    loc = result["location"]
    fout = open("D:/shequloc.txt", "a")
    fout.write(str(loc["lng"]) + ',' + str(loc["lat"]))
    fout.write('\n')
    fout.close()
    print loc["lng"], loc["lat"]

if __name__ == '__main__':
    getGeoLocation()
#     test()
    
