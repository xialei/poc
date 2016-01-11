'''
Created on 2014年4月2日

@author: Roger.xia
'''
import re
import lxml.html

def getencoding(html):
    dom = lxml.html.fromstring(html.decode('utf8', 'ignore'), parser = lxml.html.HTMLParser(remove_comments = True))
    encs = dom.xpath('.//head/meta[@charset]/@charset')
    encs += [re.findall(r'charset=(.*)', _.get('content'))[0] for _ in dom.xpath('.//head/meta[@http-equiv][@content]') if _.get('http-equiv').lower() == "content-type" and _.get('content').count('charset=') == 1]
    encs = set([_.lower() for _ in encs])
    
    if set(['gb2312', 'gbk']) <= encs: encs.remove('gb2312')
    if set(['gb2312']) == encs: encs = set(['gbk'])
    
    if len(encs) == 1: return encs.pop()

    #no encoding or multiple encoding(for web-cache sites)
    try:
        import chardet
        return chardet.detect(html)['encoding']
    except ImportError, e: raise e