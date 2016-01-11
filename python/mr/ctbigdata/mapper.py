#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from urllib import unquote

filter_w = []
f_w = open ('filterw.txt', 'r')
for w in f_w.readlines(): 
    filter_w.append(w.strip())
f_w.close()

# imput comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    # b2835964a68f246e94451078237da54e3b3a49e0,iPhone,2014-12-31 15:57:07,3101,%E5%AE%8C%E7%BE%8E%E4%B8%96%E7%95%8C,iOS7.1.2,iPhone,Mobile Safari7.0
    words = line.split(',')
    if len(words) >= 4 :
        prov_id = words[3]
        if prov_id == '3101':
            word = words[4].strip()
            word = unquote(word)
            length = len(word)
            if length >=4 and length <= 20 :
                m = re.match(r'.*(\d{7}|[A-Za-z]{5}|' + '|'.join(filter_w) + '|www\.|\.com)', word)
                if m is None :
                    print '%s\t%s' % (word, 1)