# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 10:00:32 2019

@author: Lenovo
"""

import pkuseg
import csv
import sys
import json
from gensim import corpora
from gensim import models

def EnlargeField():
    maxInt = sys.maxsize
    decrement = True
    while decrement:
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True



def CreateStopwords():
    with open("stopwords-master/百度停用词表_Chinese.txt","r",encoding='UTF-8') as stopwords_file:
        reader = stopwords_file.readlines()
        for line in reader:
            line = line[:-1]
            stopwords.append(line)
    # print(stopwords)
        
def ExcludeToken(index):
    for token in dictionaries[index]:
        if token in stopwords:
            dictionaries[index].remove(token)

def Tokenization():
    documents = []      # 文档集合
    document_num = 0
    with open("training_data/webinfo-信息检索实验数据/文档数据集.csv","r",encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            document_num += 1
            if document_num == 1:
                continue
            documents.append(line)
    print("document_num = "+str(document_num))
    seg = pkuseg.pkuseg()
    # 建立字典：从id到词项的映射
    i = 0
    for document in documents:
        tokens = seg.cut(document[3])           # 读取comment 分词
        tokens.extend(seg.cut(document[2]))     # 读取title 分词
        dictionaries[document[0]] = tokens
        ExcludeToken(document[0])
        dictionary_ids.append(document[0])
        dictionary_tokens.append(dictionaries[document[0]])
        i += 1
        print(i)
    print("Token created done!")
    # print(dictionary_ids)
    # print(dictionary_tokens)
    
def WriteToFile():
    with open('doc_token_file.txt','w',encoding='UTF-8') as doc_token_file:
        for key in dictionaries.keys():
            doc_token_file.write(key+'\n')
            for token in dictionaries[key]:
                doc_token_file.write(token+' ')
            doc_token_file.write('\n')
    print("File written!")

def Training():
    dictionary = corpora.Dictionary(dictionary_tokens)
    for doc in dictionary_tokens:
        numbered_word = dictionary.doc2bow(doc)
        numbered_words.append(numbered_word)
    # print(numbered_words)
    tf_idf = models.TfidfModel(numbered_words)
    print("Training done!")
    tf_idf.save("trained_tfidf")

def SaveDict():
    with open("dictionary_ids",'w') as f:
        json.dump(dictionary_ids,f)
    with open("dictionary_tokens",'w') as f:
        json.dump(dictionary_tokens,f)
    with open("numbered_words",'w') as f:
        json.dump(numbered_words,f)
        
EnlargeField()
dictionaries = {}
stopwords = []
dictionary_ids = []
dictionary_tokens = []
numbered_words = []
CreateStopwords()
Tokenization()
# WriteToFile()
Training()
SaveDict()