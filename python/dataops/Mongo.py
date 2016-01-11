#!/usr/bin/python
# coding: utf-8
import pymongo,sys
# conn = pymongo.Connection('localhost', 27017)
# db = conn.local
def Query(db,db2,content,field):
    counts = db[db2].find(content,field)
    return counts
def ConMongo(address='127'):
    iplist = {
              "127":['127.0.0.1', 'local'],
              "200":['192.168.250.200', 'ada'],
              "224":['192.168.0.224', 'ada'],
             }
    ip = iplist[address]
    conn = pymongo.Connection(ip[0], 27017)
    db = conn[ip[1]]
    return db

