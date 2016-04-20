#coding:utf-8

__author__ = 'apple'


import nltk
import enchant
import os,sys
import random
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout.softspace=0

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import WordPunctTokenizer
import nltk.data
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import re
import copy
from nltk.tag.sequential import ClassifierBasedPOSTagger
from nltk.corpus import treebank

from collections import OrderedDict

import pickle

from sklearn.feature_extraction.text import CountVectorizer

tokenizer = WordPunctTokenizer()

def tag_reading():
    file_object = open('Annotated_essay&newwiki.txt')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )

    all_the_text = all_the_text.decode('utf-8', 'ignore')

    p = re.compile(r'Sc\|.+')
    score = re.findall(p,all_the_text)
    #print score
    for index in range(len(score)):
        score[index] = float(score[index][3:6])

    p = re.compile(r'No\|.+')

    tagging = re.split(p,all_the_text)

    p = re.compile(r'\bE1')

    E1_number_list = []
    for item in tagging:
        E1_number = len(re.findall(p,item))
        E1_number_list.append(E1_number)

    p = re.compile(r'\bE2')
    E2_number_list = []
    for item in tagging:
        E2_number = len(re.findall(p,item))
        E2_number_list.append(E2_number)

    return score,E1_number_list,E2_number_list


def sent_tokenizer(string):
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence = []
    sentence = sentence_tokenizer.tokenize(string)
    return sentence


def word_tokenizer(string):
    tokenizer = WordPunctTokenizer()
    tokens = []
    tokens = tokenizer.tokenize(string)
    return tokens


def sentence_tokenize(sentence):
    token = tokenizer.tokenize(sentence)
    if token[-1][-1] == '.':
        token[-1] = token[-1][:-1]
        token.append('.')

    return token


def charac_counter(tokens_list):
    num = 0
    for tokens in tokens_list:
        num +=len(tokens)

    return num


def conjunc_counter(tokens_list):
    num = 0
    for tokens in tokens_list:
        if len(tokens)<4:
            num+=1
    return num


def NGSL_bagofwords_calculator(tokens_list,Dict):
    '''
    file_object = open('NGSL_lemmatized')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    Dict = all_the_text.split()
    punct = [',','.','?','!',':','\'','"']
    Dict.append(punct)

    '''



    num = 0
    #bag_of_words = [0] * len(Dict)
    for token in tokens_list:
        if token in Dict:
            num+=1

            #bag_of_words[Dict.index(token)]+=1

    return num*1.0/len(tokens_list)#,bag_of_words


def diffwords_calculator(tokens_list):
    tokens_set = set(tokens_list)

    return len(tokens_set)



#def bag_of_words()

def pos_calcu(pos_list):

    pos_tag_list = 9 * [0]
    #print pos_list
    for pos in pos_list:
        if pos[1] == 'IN':
            pos_tag_list[0]+=1
        elif pos[1][0:2] =='VB':
            pos_tag_list[1]+=1
        elif pos[1][0:2] =='NN':
            pos_tag_list[2]+=1
        elif pos[1][0:2] =='JJ':
            pos_tag_list[3]+=1
        elif pos[1][0:2] =='TO':
            pos_tag_list[4]+=1
        elif pos[1][0:2] =='DT':
            pos_tag_list[5]+=1
        elif pos[1][0:2] =='CC':
            pos_tag_list[6]+=1
        elif pos[1] ==',':
            pos_tag_list[7]+=1
        elif pos[1][0:3] =='PRP':
            pos_tag_list[8]+=1

    for index in range(len(pos_tag_list)):
        pos_tag_list[index] = pos_tag_list[index]*1.0 / len(pos_list)

    return pos_tag_list





if __name__ == '__main__':

    file_object = open('tagging_all.txt')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )

    all_the_text = all_the_text.decode('utf-8', 'ignore')

    essay_list = re.split('#@\d+', all_the_text)


    file_object = open('NGSL_lemmatized')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    Dict = all_the_text.split()
    punct = [',','.','?','!',':','\'','"']
    #Dict.append(punct)

    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(Dict)

    charac_num = [] #0. number of characters
    tokens_num = [] #1. number of tokens
    difftokens_num = [] #2. number of different tokens
    diff_to_tokens = [] #3. 2/1
    sentence_num = [] #4.number of sentences
    aver_charac = [] #5. 0/1
    aver_tokens = [] #6. 1/5
    words_in_NGSL = [] #7. ratio of words in NGSL
    E1_percent = [] #8.ratio of E1 error
    bag_of_words = [] #9.bag_of_wods

    feature_vector = []

    tokenizer = WordPunctTokenizer()


    tag = tag_reading()

    tag_list = tag[0]
    E1_num_list = tag[1]
    E2_num_list = tag[2]
    E1_num_list.pop(0)
    E2_num_list.pop(0)

    jindu = 0
    for essay_index in range(1,len(essay_list)):

        feature =[]

        essay = essay_list[essay_index]
        sentence = sent_tokenizer(essay)
        tokens = word_tokenizer(essay)

        pos = nltk.pos_tag(tokens)
        pos_tag_list = pos_calcu(pos)

        tokens_length=len(tokens)
        charac = charac_counter(tokens)
        NGSL_per = NGSL_bagofwords_calculator(tokens,Dict)


        #BOG = NGSL[1]

        diff__num = diffwords_calculator(tokens)
        short_words = conjunc_counter(tokens)


        '''

        feature.append(short_words*1.0/tokens_length)
        '''


        feature = vectorizer.transform([essay]).toarray()
        feature = list(feature[0])

        #feature = BOG


        for x in  pos_tag_list:
            feature.append(x)

        feature.append(len(sentence))#4
        feature.append(tokens_length) #1
        feature.append(charac) #0
        feature.append(charac*1.0/tokens_length) #5
        feature.append(tokens_length*1.0/len(sentence))
        feature.append(E1_num_list[essay_index-1]*1.0/tokens_length) #8
        feature.append(E2_num_list[essay_index-1]*1.0/tokens_length) #8
        feature.append(NGSL_per)
        feature.append(diff__num)
        feature.append(diff__num*1.0/tokens_length)



        feature_vector.append(feature)
        print jindu
        jindu+=1


    print charac_num
    print tokens_num
    print difftokens_num  #2. number of different tokens
    print diff_to_tokens  #3. 2/1
    print sentence_num  #4.number of sentences
    print aver_charac  #5. 0/1
    print aver_tokens #6. 1/5
    print words_in_NGSL  #7. ratio of words in NGSL
    print E1_percent  #8.ratio of E1 error
    print bag_of_words  #9.bag_of_wods

    print feature_vector

    f=open('feature_vector_BOGPOS(new).txt','w')
    pickle.dump(feature_vector,f,0)
    f.close()

    '''
    f=open('tag_list_all(new).txt','w')
    pickle.dump(tag_list,f,0)
    f.close()
    '''


    '''

    answer = tag_reading()

    print answer[0]
    print answer[1]
    '''

    '''
    FV: 第一批特征

    02:  5，6，7，3
    03:FV ＋ E2
    04:FV + E2 + short_words
    05: 04 - 2,1,0




    FV_ALL:  FV+E2
    FV_ALL_1 : FV+E2+short_words
    feature_vector_all_POS.pkl FV + E2 +POS
    '''