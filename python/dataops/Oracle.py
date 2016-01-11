#!/usr/bin/python
# coding: utf-8
import cx_Oracle
conn=cx_Oracle.connect('JUCHAO/chinascope1234@122.144.134.2:1521/csdb001')    #连接数据库
cursor=conn.cursor()

def OracleSql(Sql):
    cursor.execute(Sql)              
    Res=cursor.fetchall()
    return Res
    cursor.close()
    conn.close()
    
