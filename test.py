# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 20:02:40 2019

@author: Lenovo
"""

import pkuseg
import csv
import sys
import json
from gensim import corpora
from gensim import models
import numpy as np

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

def CreateQueryDictionary():
    tf_idf = models.TfidfModel.load("trained_tfidf")
# =============================================================================
#     with open('doc_token_file.txt','r',encoding='UTF-8') as doc_token_file:
#         reader = doc_token_file.readlines()
#         line_num = 0
#         for line in reader:
#             if line_num % 2 == 0:
#                 dictionary_ids.append(line[:-1])
#             else:
#                 words = line.split()
#                 dictionary_tokens.append(words)
#             line_num += 1
#             print(line_num)
# =============================================================================
            #if line_num > 201:
            #    break
    # print(dictionary_ids)
    # print(dictionary_tokens)
    dictionary = corpora.Dictionary(dictionary_tokens)
    token_id_dictionary.update(dictionary.token2id)
    i = 0
    for doc in dictionary_tokens:
#        numbered_word = dictionary.doc2bow(doc)
        words_idf = dict(tf_idf[numbered_words[i]])
        words_idf_dictionary.append(words_idf)
        i += 1
    print("QueryDictionary Created!")

def LoadQueryItems():
    document_num = 0
    with open("test_data/test_querys.csv", "r", encoding = 'UTF-8') as queryfile:
        reader = csv.reader(queryfile)
        for line in reader:
            document_num += 1
            if document_num == 1:
                continue
            queries_name.append(line[0])
            queries_id.append(line[1])
        print(document_num)
        print(queries_id)
        print(queries_name)
        print("LoadQueryItems Complete!")

def Query():
    seg = pkuseg.pkuseg()
    with open("stopwords-master/百度停用词表_Chinese.txt","r",encoding='UTF-8') as stopwords_file:
        reader = stopwords_file.readlines()
        for line in reader:
            stopwords.append(line[:-1])
            
    with open("submission.csv", "w", encoding='UTF-8') as submissionfile:
        writer = csv.writer(submissionfile)
        output = ["query_id","doc_id"]
        writer.writerow(output)

    #    request = input("Request:")
        for query_index in range(0, len(queries_id)) :
            print("query_index = "+str(query_index))
    #        while request != '0' :
            request = queries_name[query_index]
            query_tokens = seg.cut(request)     # 分词
            for token in query_tokens:          # 删去停用词
                if token in stopwords:
                    query_tokens.remove(token)
            print(query_tokens)
            dimension = len(query_tokens)
            query_vector = np.ones(dimension)
            # 开始遍历文档，求每个文档的向量，并求余弦距离，放入字典中
            cosine_map = {}
            index = 0
            while index < len(dictionary_ids) :
                doc_vector = []
                for token in query_tokens:
                    if token in token_id_dictionary:
                        token_id = token_id_dictionary[token]
                        if token_id in words_idf_dictionary[index].keys() :
                            token_tfidf = words_idf_dictionary[index][token_id]
                            # print(token_tfidf)
                            doc_vector.append(token_tfidf)
                        else:
                            doc_vector.append(0)
                    else:
                        doc_vector.append(0)
                # doc_vector为doc的向量
                doc_vector = np.array(doc_vector)
                # 下面求余弦距离
                cosine = Cosine(query_vector,doc_vector)
                if cosine != 0:
                    new_dicvalue = {np.linalg.norm(doc_vector):dictionary_ids[index]}
                    if cosine not in cosine_map.keys():
                        cosine_map[cosine] = {}
                    cosine_map[cosine].update(new_dicvalue)
                index += 1
                print(index)
            # 对cosine字典按键反向排序
            cosine_sorted = sorted(cosine_map,reverse=True)
            print(cosine_sorted)

            print("query_index = "+str(query_index))
            
            i = 0
            j = 0
            counter_map = 0
            output_set = sorted(cosine_map[cosine_sorted[counter_map]], reverse=True)
            output_20 = []       
            while i < 20:
                temp = (cosine_map[cosine_sorted[counter_map]])[output_set[j]]
                j += 1
                i += 1
                output_20.append(temp)
                if j == len(cosine_map[cosine_sorted[counter_map]]):
                    counter_map += 1
                    j = 0
                    output_set = sorted(cosine_map[cosine_sorted[counter_map]], reverse=True)
            print(output_20)
            for i in range(0, 20):
                write_temp = []
                write_temp.append(queries_id)
                write_temp.append(output_20[i])
                writer.writerow(write_temp)                
                
    #            request = input("Request:")

def Cosine(vector_a,vector_b):
    if np.all(vector_a == 0) or np.all(vector_b == 0):
        cos = 0
    else:
        mul = np.dot(vector_a,vector_b)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = mul / denom
    return cos

def LoadDict():
    global dictionary_ids, dictionary_tokens, numbered_words
    with open("dictionary_ids",'r') as f:
        dictionary_ids = json.load(f)
    with open("dictionary_tokens",'r') as f:
        dictionary_tokens = json.load(f)
    with open("numbered_words",'r') as f:
        numbered_words = json.load(f)
    print("Load Done!")

EnlargeField()
stopwords = []
numbered_words = []
dictionaries = {}
dictionary_ids = []
dictionary_tokens = []
token_id_dictionary = {}
words_idf_dictionary = []
queries_name = []
queries_id = []
LoadQueryItems()
LoadDict()
CreateQueryDictionary()
Query()