__author__ = 'xialei'

# -*- coding: utf-8 -*-

import os
import jieba
import string
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import sys

reload(sys)
sys.setdefaultencoding('utf8')

print sys.getdefaultencoding()


def getFilelist(path):
    filelist = []
    files = os.listdir(path)
    for f in files:
        if f[0] == '.':
            pass
        else:
            fp = path + '/' + f
            if os.path.isdir(fp):
                filelist.extend(getFilelist(fp)[0])
            else:
                if f[0] == '.':
                    pass
                else:
                    filelist.append(fp)
    return filelist, path


def seg(file, path):
    # save seg file
    sfile = path + '../segfile'
    if not os.path.exists(sfile):
        os.mkdir(sfile)
    f = open(file, 'r+')
    file_list = f.read()
    f.close()

    seg_list = jieba.cut(file_list, cut_all=True)

    result = []
    for seg in seg_list:
        seg = ''.join(seg.split())
        if (seg != '' and seg != "\n" and seg != "\n\n"):
            result.append(seg)

    f = open(sfile + "/" + file.split('/')[-1] + "-seg.txt", "w+")
    f.write(' '.join(result).encode('utf-8'))
    f.close()


def cal_tfidf(path):
    segdir = path + "../segfile/"
    files = os.listdir(segdir)
    corpus = []
    for ff in files:
        f = open(segdir + ff, 'r')
        content = f.read()
        f.close()
        corpus.append(content)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfi = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()
    weight = tfi.toarray()

    sfile = dir + '../tfidffile'
    if not os.path.exists(sfile):
        os.mkdir(sfile)

    for i in range(len(weight)):
        f = open(sfile + '/' + string.zfill(i, 5) + '.txt', 'w+')
        for j in range(len(word)):
            f.write(word[j].encode('utf-8') + "\t" + str(weight[i][j]) + "\n")
        f.close()


if __name__ == "__main__":
    dir = '/Users/xialei/workspace/data/files/'

    # (allfile, path) = getFilelist(dir)

    # for f in allfile :
    #     seg(f, path)

    cal_tfidf(dir)
