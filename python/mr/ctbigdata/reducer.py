'''
Created on 2015-6-4

@author: Roger.xia
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# read input from mapper.py and compute freq of words
# hadoop fs -cat /ctbigdata/shanghai/12/all/All_201501010759_99.txt |python mapper.py |python reducer.py
# hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar -jobconf mapred.reduce.tasks=4 -mapper mapper.py -file /home/xxx/mapper.py -reducer reducer.py -file /home/xxx/reducer.py -file /home/xxx/stock.txt -input /ctbigdata/shanghai/12/all/All_201501010759_99.txt -output /user/xxx/output/

from operator import itemgetter
import sys
import re

secuw = []
f_secu = open ('securityw.txt', 'r')
for w in f_secu.readlines(): 
    secuw.append(w.strip())
f_secu.close()

# maps words to their count
word2count = {}

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    
    try:
        # parse the input we got
        word,count = line.rsplit('\t', 1)
        count = int(count)
        
        m = re.match(r'(.*)(' + '|'.join(secuw) + ')', word)
        if m is None :
            word2count[word] = word2count.get(word, 0) + count
        else :
            prefix_w = m.group(1).strip()
            if word2count.has_key(prefix_w) :
                word2count[prefix_w] = word2count.get(prefix_w, 0) + count
    except ValueError:
        # ignore this line
        # print line
        pass

sorted_stock2count = sorted(word2count.items(), key=itemgetter(0))

# get securities
stocks = []
f_stock = open ('stock.txt', 'r')
for secu in f_stock.readlines(): 
    stocks.append(secu.strip())
f_stock.close()

# write the result to STDOUT or file for test
for word, count in sorted_stock2count:
    match = re.match(r'.*(' + '|'.join(stocks) + ')', word)
    if match is not None :
        print '%s\t%s' % (word, count)
