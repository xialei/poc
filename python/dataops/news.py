# -*- coding: utf-8 -*- 

import re

import jieba
import word2vec
import codecs

from tools import mongoclient
from gensim import corpora, models
from gensim.models import LdaModel
from gensim.corpora import Dictionary

def generate_news_file(db):

    hnews = db['hotnews_analyse']
    
    resultset = hnews.find()
    
    f = open("news.txt", 'w')
    
    n = 0
    str_row = ""
    
    for row in resultset:
        t = row.get("t", "")
        dt = row.get("dt", "")
        a = row.get("auth", "")
        s = row.get("sum", "").replace("#&#", "")
        
        str_row = str_row + dt + "\t" + t + "\t" + a + "\t" + s + "\n"
        
        n = n + 1
        
        if n % 5000 == 0 :
            f.write(str_row.encode('utf-8'))
            n = 0
            str_row = ""
            print "----"
    
    f.close()

def cleanText():
    f = open("news.txt", 'r')
    fs = open("summary.txt", "w+")
    lines = f.readlines()
    for line in lines:
        parts = line.split("\t")
        text = parts[1] + " " + parts[3] + "\n"
        fs.write(text)
    fs.close()
    f.close()
    
# jieba支持三种分词模式：
# 　　＊精确模式，试图将句子最精确地切开，适合文本分析；
# 
# 　　＊全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
# 
# 　　＊搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
# 
# 主要采用以下算法：
# 
# 　　＊基于Trie树结构实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图（DAG)
# 
# 　　＊采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合
# 
# 　　＊对于未登录词，采用了基于汉字成词能力的HMM模型，使用了Viterbi算法
# 
# 注意：
#     用jieba切词（试了不少词库发现效果都没自带的dict.txt.big，开启hmm效果好）；
#     用u'([\u4E00-\u9FA5a-zA-Z0-9+_]+)'去掉特殊字符和标点（注意因为是unicode范围，输入word需要decode('utf8')）；
#     (word2vec可选) 用stop_words表去停用词，因为后续doc2vec也会用到
def tokenizer():
    f = open("summary.txt", 'r')
    fw = open("segs.txt", "w+")
    lines = f.readlines()
    for line in lines:
        seg_list = jieba.cut(line, cut_all=False)  # True for full pattern, False for accurate pattern.
        segs = ' '.join(seg_list) + "\n"
        fw.write(segs.encode('utf-8'))
    fw.close()
    f.close()

def wordvec():
    # 少于min_count次数的单词会被丢弃掉
    word2vec.word2vec('D:\nlp\corpora\segs.txt', 'vectors.bin', size=100, window=10, sample='1e-3', hs=1, negative=0, threads=12, iter_=5, min_count=10, binary=1, cbow=0, verbose=True)
    # word2vec.doc2vec('D:\nlp\corpora\segs.txt', 'D:\work\poc\python\dataops\vectors.bin', size=100, window=10, sample='1e-4', hs=1, negative=0, threads=12, iter_=20, min_count=1, binary=1, cbow=0, verbose=True)

def lda():
    # remove stop words
    stopwords = codecs.open('../conf/stop_words_ch.txt', mode='r', encoding='utf8').readlines()
    stopwords = [ w.strip() for w in stopwords ]
    
    fp = codecs.open('D:\\nlp\corpora\segs.txt', mode='r', encoding='utf8')
    train = []
    for line in fp:
        line = line.split()
        train.append([ w for w in line if w not in stopwords ])
    
    dictionary = corpora.Dictionary(train)
    corpus = [ dictionary.doc2bow(text) for text in train ]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=100)
    
    lda.print_topics(30)
    # print topic id=20
    lda.print_topic(20)
    
    # save/load model
    lda.save('D:\\nlp\corpora\news.model')
    #     lda = LdaModel.load('D:\nlp\corpora\news.model')

def test():
    s = "中国, 你好 ！   伟大 的  祖国. a 8"
    rule = r'[\u4e00-\u9fa5a-zA-Z0-9+_]'
    punct = set(u'''的:!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
    
    print re.sub(rule, r'', s)
    print filter(lambda x: x not in punct, s.decode('utf-8'))
    
if __name__ == "__main__":
    # generate_news_file(mongoclient.get_db())
    # cleanText()
    # tokenizer()
    # wordvec()
    lda()
    # test()
