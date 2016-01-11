# -*- coding: utf-8 -*-

'''
Created on 2015年6月10日

@author: Roger.xia
'''

from random import random

def random_shuffle(A):
    length = len(A)
    for i in range(0, length):
        randomi = int(random()*length)
        print randomi
        A[i],A[randomi] = A[randomi],A[i]
    return A

if __name__ == '__main__' :
    A = [1,2,3,4,5]
    B = random_shuffle(A)
    print B