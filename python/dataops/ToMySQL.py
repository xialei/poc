#!/usr/bin/python
# coding: utf-8
import mysql.connector, sys, re, platform
import file

CONFIG208 = {
            'host': '192.168.250.208',
            'user': 'ada_user',
            'passwd':'ada_user',
            'db':'ada-fd',
            
            } 
CONFIGLocal = {
            'host': '127.0.0.1',
            'user': 'root',
            'passwd':'root)(*&',
            'db':'gg',
            'client_flags': [mysql.connector.ClientFlag.LOCAL_FILES] 
        }
ConnLocal = mysql.connector.connect(**CONFIGLocal)
Conn208 = mysql.connector.connect(**CONFIG208)


def SqlExec(sql, Local=1, Log=''):
    try:
        if Local == 1:
            conn = ConnLocal
        else:
            conn = Conn208
    except :
        print("mysql连接错误,Local={0}" .format(Local))
        print("错误:{0}".format(sys.exc_info()[1]))
        sys.exit()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except:
        file.ToLog("错误SQL语句:{0}".format(sql))
        file.ToLog("错误提示:{0}".format(sys.exc_info()[1]))
        sys.exit()
    if cursor.rowcount == -1:  # 读取操作
        SqlResult = cursor.fetchall()
        return SqlResult
    else:  #
        print(" 完成{:,}条".format(cursor.rowcount))


    
def SqlCommend(commend, Local=1):
    return SqlExec(commend, Local)
