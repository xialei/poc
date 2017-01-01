# -*- coding: utf-8 -*-
'''
Created on 2017年1月1日

@author: xialei
'''
import urllib2
import StringIO
import gzip

def getResponseHtml(url):
    try:
        request = urllib2.Request(url)
        request.add_header('Accept-Encoding', 'gzip')
        response = urllib2.urlopen(request)
        data = response.read()
        response.close()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            data = StringIO.StringIO(data)
            gzipper = gzip.GzipFile(fileobj=data)
            html = gzipper.read()
            gzipper.close()
        else:
            html = data
        # html = html.decode('GBK').encode('utf-8')
        return html
    except Exception, e:
        print "No content for ", url, e
    return None

if __name__ == '__main__':
    pass