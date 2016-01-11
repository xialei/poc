#!/usr/bin/python
# coding: utf-8
from collections import OrderedDict
from pandas import Series, DataFrame
import os, hashlib, sys, datetime, shutil
import xlrd
import win32clipboard as w
import win32con
 
def GetCopyText():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT).decode('utf-16le')
    w.CloseClipboard()
    return d
 
def CopyText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardText( aString,win32con.CF_TEXT)
#     print (w.GetClipboardData(win32con.CF_TEXT))
    w.CloseClipboard()
# CopyText('a')
def ToLog(content):
    rootindex = os.path.dirname(sys.path[0])
    logpath = rootindex + '/log.log'
    fp = open(logpath, mode='a', encoding='utf-8')
    LogContent = "%s,%s\n" % (datetime.datetime.now(), content)
    fp.write(LogContent)
    fp.close()
    print(content)

def WriteACSV(Path, Data, Mode, Code='utf-8'):
    fp = open(Path, mode=Mode, encoding=Code)
    fp.write(Data)
    fp.close()

def TmpToFile(TmpPath, Path):
    TmpFile = open(TmpPath, mode="r", encoding='utf-8')
    thisfile = TmpFile.read()
    TmpFile.close()
    File = open(Path, mode="a", encoding='utf-8')
    File.write(thisfile)
    File.close()
    DelFile(TmpPath)

def WriteOnce(RowCount, content, Path, EachRowToWrite=10000):
    if RowCount % EachRowToWrite == 0 and RowCount / EachRowToWrite > 0:
            print('time:{0} 完成:{1}行解析'.format(datetime.datetime.now().strftime('%H:%M:%S'),RowCount))
            try:
                WriteACSV(Path, content, "a")
            except:
                print('err')
                WriteACSV(r'D:/temp.txt', content, "a")
            content = ''
    return content

def CountI(I):
    EachRowToWrite = 100000
    if I % EachRowToWrite == 0 and RowCount / EachRowToWrite > 0:
        print('完成:{:,}行解析'.format(RowCount))
        print ('time:{0}'.format(datetime.now().strftime('%H:%M:%S')))

def WriteLine(This, Total):
    EachLine = 100
    if This % EachLine == 0 and EachLine / EachLine > 0:
            print("完成:{0} of {1}".format(This, Total))
            
def WriteFinish(RowCount, content, Path):
    WriteACSV(Path, content, 'a')
    print('完成:{:,}行解析'.format(RowCount))

def DelFile(savrpath):
    if os.path.isfile(savrpath):
        os.remove(savrpath)
def IsExist(savrpath):
    if os.path.isfile(savrpath):
        return True
    else:
        return False
            
def OpenDict(DictPath, key=0, val=1, lower=0, DictSplit='^', HasTitle=0, Code='utf-8'):
    Dict = OrderedDict()
    DictFile = open(DictPath, 'r', encoding=Code)
    DictFileTxt = DictFile.read().replace("\ufeff", "").split('\n')
    if DictFileTxt[len(DictFileTxt) - 1] == '':
        DictFileTxt = DictFileTxt[0:len(DictFileTxt) - 1]
    DictFileTxt = DictFileTxt[HasTitle:]
    for DictLine in DictFileTxt:
        DictObj = DictLine.split(DictSplit)
        if DictObj[0][0:1] != "#":
            if lower == 1:
                Dict[DictObj[key].lower()] = DictObj[val]
            else:
                Dkey = DictObj[key]
                if isinstance(val, list):
                    Dval = []
                    for i in val:
                        Dval.append(DictObj[i])
                elif val=='All':
                    Dval = []
                    del DictObj[key]
                    for ValAll in DictObj:
                        Dval.append(ValAll)
                else:    
                    Dval = DictObj[val]
                Dict[Dkey] = Dval
    return Dict

    
    
def DictSplit(Path):
    if Path[-4:] == 'acsv':
        DictSplit = '^'
    else:
        DictSplit = '\t'
    return  DictSplit

def OpenFile(FilePath):
    DictFile = open(FilePath, 'r', encoding='utf-8')
    DictFileTxt = DictFile.read().replace("\ufeff", "").split('\n')
    if DictFileTxt[len(DictFileTxt) - 1] == '':  # "��1行是空白，去除list"��"��"
        DictFileTxt = DictFileTxt[0:len(DictFileTxt) - 1]
    return DictFileTxt

def OpenList(FilePath, Val, NonRepeat=False, HasTitle=0, DictSplit='^', Code='utf-8'):
    Rlist = []
    DictFile = open(FilePath, 'r', encoding=Code)
    DictFileTxt = DictFile.read().replace("\ufeff", "").split('\n')
    if DictFileTxt[len(DictFileTxt) - 1] == '': 
        DictFileTxt = DictFileTxt[0:len(DictFileTxt) - 1]
    DictFileTxt = DictFileTxt[HasTitle:]
    for DictLine in DictFileTxt:
        tlist = DictLine.split(DictSplit)
        if Val!='All':
            Rlist.append(tlist[Val])
        else:
            Rlist.append(tlist)
    if NonRepeat:
        Rlist = list(set(Rlist))
    return Rlist
  
    
def WirteDict(DictPath, DictContent):
    DictDic = ''
    for Dictone in DictContent:
        DictDic += "{1}{0}{2}\n".format("\t", Dictone, DictContent[Dictone])
    WriteACSV(DictPath, DictDic, 'w')


    
def SQLtoVar(sqlresult):
    NewVar = sqlresult[0][0]
    return NewVar 

def SQLtoOneLine(sqlresult):
    NewLine = sqlresult[0]
    return NewLine  
 
def SQLtoMultLine(sqlresult):
    NewLine = sqlresult[0]
    return NewLine  
 
def SQLtoList(sqlresult, col):
    NewList = []
    for res in sqlresult:
        NewList.append(res[col])
    return NewList

    return NewList
def SQLtoDict(sqlresult, k=0, v=1):
    NewDict = OrderedDict()
    for res in sqlresult:
        key = res[k]
        value = res[v]
        NewDict[key] = value
    return NewDict

def md5(iname):
    m = hashlib.md5(iname.encode("utf8"))
    return m.hexdigest()
def AddTag(Path, line, tag):
    ReadFile = open(Path, mode="r", encoding='utf-8')
    thisfile = ReadFile.read()
    ReadFile.close()
    thisfile = thisfile.replace(line, tag + line)
    WriteFile = open(Path, mode="w", encoding='utf-8')
    WriteFile.write(thisfile)
    WriteFile.close()
    
def OpenExcel(Path, sheet_name):   
    data = xlrd.open_workbook(Path)
    table = data.sheet_by_name(sheet_name)
    return table

def ExcelToList(Path, Key=0, HasTitle=1, StName='Sheet1'):
    ExcelList = []
    table = OpenExcel(Path, StName)
    nrows = int(table.nrows)
    for i in range(HasTitle, nrows):
        if isinstance(Key, list):
            Value = []
            for V in Key:
                Value.append(table.cell(i, V).value)
            ExcelList.append(Value)
        else:
            if table.cell(i, Key).value == '':
                a = 1
            else:
                ExcelList.append(table.cell(i, Key).value)
    return ExcelList

def ExcelToSeries(Path, Key=0, Val=1, HasTitle=1, StName='Sheet1'):
    i = 0
    ExcelSeries = Series()
    table = OpenExcel(Path, StName)
    nrows = int(table.nrows)
    for i in range(HasTitle, nrows):
        if table.cell(i, Key).value == table.cell(i, Val).value == '':
            a = 1
        else:
            str1 = table.cell(i, Key).value
            str2 = table.cell(i, Val).value
            ExcelSeries[str(i)] = str1 + ',' + str2
            i += 1
    return ExcelSeries

def ExcelToDict(Path, Key=0, Val=1, HasTitle=1, StName='Sheet1'):  # 0开始,不是1
    ExcelDict = OrderedDict()
    table = OpenExcel(Path, StName)
    nrows = int(table.nrows)
    for i in range(HasTitle, nrows):
        if table.cell(i, Key).value == '':
            a = 1
        else:
            if isinstance(Val, list):
                Value = []
                for V in Val:
                    Value.append(table.cell(i, V).value)
                    try:
                        ExcelDict[table.cell(i, Key).value] = Value
                    except:
                        print('Err', table.cell(i, Key).value, Value)
            else:
                ExcelDict[table.cell(i, Key).value] = table.cell(i, Val).value
    return ExcelDict
def CopyFile(From, To):
    shutil.copy (From, To)


def FileRepalce(Path, Dict, DictSplit='\t'):
    Path = r'D:\web\Python\work\mongo\gg\renrou.txt'
    Dict = r'D:\web\Python\work\mongo\gg\renrou_rep.txt'
    Rep1 = OpenDict(Dict)
    Rep2 = OpenDict(Dict, 0, 2)
    NewFile = ''
    with open(Path, encoding='utf-8') as myfile:
        for line in myfile:
            Sd = line.split(DictSplit)
            if Sd[0] in Rep1:
                line = DictSplit.join([Sd[0], Rep1[Sd[0]], Rep2[Sd[0]]]) + '\n'
            NewFile += line
    WriteACSV(Path, NewFile, 'w')
# FileRepalce(1,2)   
def Pnow(Status):
    print ('{0} : {1}'.format(Status, datetime.datetime.now().strftime('%H:%M:%S')))
