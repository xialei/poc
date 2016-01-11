# encoding=utf-8
'''
Created on 2014年4月1日

@author: Roger.xia
'''

import csv

def write_list_to_csv(fn, data):
    with open(fn, mode='wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            csv_writer.writerow([col.encode('utf8') for col in row])
        
def append_list_to_csv(fn, data):
    with open(fn, mode='a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)