#coding:utf-8

__author__ = 'apple'

import cPickle
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout.softspace=0


import Scoring_training as Sc
from Word_inspector import Words_inspector as insp
from Word_inspector import Main
from Word_inspector import Tokenizer
import feature_extractor as Fe
import copy
import re
import os

basedir = str(os.getcwd())+ '/learn/English/'

def getdir():
    file_object = open(basedir + 'text_file/input_essay.txt')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close()

    essay = all_the_text.decode('utf-8', 'ignore')
    return essay



def input_initialization():

    print 'Loading essay...'
    file_object = open('text_file/input_essay.txt')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close()

    essay = all_the_text.decode('utf-8', 'ignore')
    return essay


def replace(string):

    string = re.sub(u'\u2019', '\'', string)

    return string


def dict_initialization():

    print 'Loading NGSL Dictionary...'
    file_object = open(basedir + 'NGSL_lemmatized')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )

    Dict = all_the_text.split()
    return Dict


def classifier_initialization():

    print 'Initiating classifiers...'

    f=open(basedir + 'Classifiers/LR(all+pos).pkl','r')
    regr = cPickle.load(f)

    f=open(basedir + 'Classifiers/MAXENT_prep_classifier_new.pkl','r')
    clf1 = cPickle.load(f)


    f = open(basedir + 'Classifiers/linearSVC.pkl','r')
    clf2 = cPickle.load(f)

    return regr, clf1, clf2



def classifier_initialization2():

    print 'Initiating classifiers...'

    f=open(basedir + 'Classifiers/LR(all+pos).pkl','r')
    regr = cPickle.load(f)

    f=open(basedir + 'Classifiers/MAXENT_prep_classifier_new.pkl','r')
    clf1 = cPickle.load(f)


    f = open(basedir + 'Classifiers/linearSVC_newfeature_(50k)_5.pkl','r')
    clf2 = cPickle.load(f)

    return regr, clf1, clf2



def classifier_initialization3():

    print 'Initiating classifiers...'

    f=open(basedir + 'Classifiers/LR(all+pos).pkl','r')
    regr = cPickle.load(f)

    f=open(basedir + 'Classifiers/MAXENT_prep_classifier_new.pkl','r')
    clf1 = cPickle.load(f)


    f = open(basedir + 'Classifiers/linearSVC_BOBi_(160k)_5.pkl','r')
    clf2 = cPickle.load(f)

    return regr, clf1, clf2


Dict = dict_initialization()
regr, clf1, clf2 = classifier_initialization2()
tokenizer = Sc.WordPunctTokenizer()
#essay = input_initialization()
vectorizer_ALL = Fe.Vectorizer_initialization2()


def round_score(x):
    x = round(x * 2 )*1.0/2

    if x > 6.0:
        x = 6.0
    if x < 0.0:
        x = 0.0

    return x


def basic_statistic(essay):

    print 'Doing basic statistic...'

    sentence = Sc.sent_tokenizer(essay)

    string = ''

    for x in sentence:
        string += x + ' '

    tokens = Sc.word_tokenizer(essay)

    if len(sentence)<2 or len(tokens)<10:
        return 0,0,0,0,0,0

    sentence_tokens = Tokenizer.both_tokenizer(sentence)
    sentence_tokens2 = copy.deepcopy(sentence_tokens)

    pos = Sc.nltk.pos_tag(tokens)
    pos_tag_list = Sc.pos_calcu(pos)

    TOKEN_list = []
    for token in sentence_tokens:
        if token[-1][-1] == '.':
            token[-1] = token[-1][:-1]
            token.append('.')
        TOKEN_list.append(token)
    POS_list = []

    for sent in TOKEN_list:
        POS_list.append(Sc.nltk.pos_tag(sent))


    return sentence,tokens,sentence_tokens2,pos_tag_list,TOKEN_list,POS_list,string


def Scoring_feature_extraction(tokens,Dict,sentence,pos_tag_list,TOKEN_list,POS_list,regr,clf1,clf2,vectorizer_ALL):

    print 'Inspecting words spelling...'



    E1_list = insp.words_inspector(tokens)

    print 'Inspecting preposition usage...'






    E2_list1 = []
    T2_list1 = []
    E2_list2 = []
    T2_list2 = []

    E2_list = []

    for sent in range(len(TOKEN_list)):
        Flag1 = True
        index = Fe.Preposition_indexing(TOKEN_list[sent])
        temp = copy.deepcopy(POS_list[sent])
        for x in index:
            feature_temp = Fe.Preposition_usage1_extractor(temp,x)
            if clf1.classify(feature_temp) == 'False':
                Flag1 = False
                E2_list1.append((sent,x,TOKEN_list[sent][x],'False'))
                E2_list.append(sent)
            else:
                T2_list1.append((sent,x,TOKEN_list[sent][x],'True'))
            temp = copy.deepcopy(POS_list[sent])



        if clf2.predict(Fe.preosition_usage2_extractor(POS_list[sent], vectorizer_ALL)) == 'False':
            Flag1 = False
            E2_list2.append((sent,'False'))
            E2_list.append(sent)
        else:
            T2_list2.append((sent,'True'))

    #print E2_list1,T2_list1

    #print E2_list2,T2_list2

    E2_list = list(set(E2_list))




    print 'Extracting scoring features...'

    tokens_length=len(tokens)
    charac = Sc.charac_counter(tokens)
    NGSL_per = Sc.NGSL_bagofwords_calculator(tokens,Dict)
    diff__num = Sc.diffwords_calculator(tokens)
    #short_words = Sc.conjunc_counter(tokens)

    feature = []


    for x in pos_tag_list:
        feature.append(x)

    feature.append(len(sentence))#4
    feature.append(tokens_length) #1
    feature.append(charac) #0
    feature.append(charac*1.0/tokens_length) #5
    feature.append(tokens_length*1.0/len(sentence))

    feature.append(len(E1_list)*1.0/tokens_length) #8
    feature.append(len(E2_list)*1.0/tokens_length) #

    feature.append(NGSL_per)
    feature.append(diff__num)
    feature.append(diff__num*1.0/tokens_length)


    Final_score = round_score(regr.predict(feature))
    return Final_score,E1_list, E2_list, E2_list1, E2_list2





def Scoring_feature_extraction2(tokens,sentence,pos_tag_list,TOKEN_list,POS_list):

    print 'Inspecting words spelling...'

    E1_list = insp.words_inspector(tokens)

    print 'Inspecting preposition usage...'

    #print tokens
    #print E1_list




    E2_list1 = []
    T2_list1 = []
    E2_list2 = []
    T2_list2 = []

    E2_list = []

    for sent in range(len(TOKEN_list)):
        Flag1 = True
        index = Fe.Preposition_indexing(TOKEN_list[sent])
        temp = copy.deepcopy(POS_list[sent])
        for x in index:
            feature_temp = Fe.Preposition_usage1_extractor(temp,x)
            if clf1.classify(feature_temp) == 'False':
                Flag1 = False
                E2_list1.append((sent,x,TOKEN_list[sent][x],'False'))
                E2_list.append(sent)
            else:
                T2_list1.append((sent,x,TOKEN_list[sent][x],'True'))
            temp = copy.deepcopy(POS_list[sent])



        if clf2.predict(Fe.preosition_usage2_extractor2(POS_list[sent], vectorizer_ALL)) == 'False':
            Flag1 = False
            E2_list2.append((sent,'False'))
            E2_list.append(sent)
        else:
            T2_list2.append((sent,'True'))

    #print E2_list1,T2_list1

    #print E2_list2,T2_list2

    E2_list = list(set(E2_list))




    print 'Extracting scoring features...'

    tokens_length=len(tokens)
    charac = Sc.charac_counter(tokens)
    NGSL_per = Sc.NGSL_bagofwords_calculator(tokens,Dict)
    diff__num = Sc.diffwords_calculator(tokens)
    #short_words = Sc.conjunc_counter(tokens)

    feature = []


    for x in pos_tag_list:
        feature.append(x)

    feature.append(len(sentence))#4
    feature.append(tokens_length) #1
    feature.append(charac) #0
    feature.append(charac*1.0/tokens_length) #5
    feature.append(tokens_length*1.0/len(sentence))

    feature.append(len(E1_list)*1.0/tokens_length) #8
    feature.append(len(E2_list)*1.0/tokens_length) #

    feature.append(NGSL_per)
    feature.append(diff__num)
    feature.append(diff__num*1.0/tokens_length)


    Final_score = round_score(regr.predict(feature))
    return Final_score,E1_list, E2_list, E2_list1, E2_list2





def Scoring_feature_extraction3(tokens,Dict,sentence,pos_tag_list,TOKEN_list,POS_list,regr,clf1,clf2,vectorizer_ALL):

    print 'Inspecting words spelling...'

    E1_list = insp.words_inspector(tokens)

    print 'Inspecting preposition usage...'






    E2_list1 = []
    T2_list1 = []
    E2_list2 = []
    T2_list2 = []

    E2_list = []

    for sent in range(len(TOKEN_list)):
        Flag1 = True
        index = Fe.Preposition_indexing(TOKEN_list[sent])
        temp = copy.deepcopy(POS_list[sent])
        for x in index:
            feature_temp = Fe.Preposition_usage1_extractor(temp,x)
            if clf1.classify(feature_temp) == 'False':
                Flag1 = False
                E2_list1.append((sent,x,TOKEN_list[sent][x],'False'))
                E2_list.append(sent)
            else:
                T2_list1.append((sent,x,TOKEN_list[sent][x],'True'))
            temp = copy.deepcopy(POS_list[sent])



        if clf2.predict(Fe.preosition_usage2_extractor3(sentence[sent], vectorizer_ALL)) == 'False':
            Flag1 = False
            E2_list2.append((sent,'False'))
            E2_list.append(sent)
        else:
            T2_list2.append((sent,'True'))

    print E2_list1,T2_list1

    print E2_list2,T2_list2

    E2_list = list(set(E2_list))




    print 'Extracting scoring features...'

    tokens_length=len(tokens)
    charac = Sc.charac_counter(tokens)
    NGSL_per = Sc.NGSL_bagofwords_calculator(tokens,Dict)
    diff__num = Sc.diffwords_calculator(tokens)
    #short_words = Sc.conjunc_counter(tokens)

    feature = []


    for x in pos_tag_list:
        feature.append(x)

    feature.append(len(sentence))#4
    feature.append(tokens_length) #1
    feature.append(charac) #0
    feature.append(charac*1.0/tokens_length) #5
    feature.append(tokens_length*1.0/len(sentence))

    feature.append(len(E1_list)*1.0/tokens_length) #8
    feature.append(len(E2_list)*1.0/tokens_length) #

    feature.append(NGSL_per)
    feature.append(diff__num)
    feature.append(diff__num*1.0/tokens_length)


    Final_score = round_score(regr.predict(feature))
    return Final_score,E1_list, E2_list, E2_list1, E2_list2



def printer(E2_list,E2_list1,E2_list2,Final_score,sentence):
    suggestion = ''
    for x in E2_list1:
        suggestion += '第'+str(x[0]+1)+'句句子:\n'+ sentence[x[0]] +'\n第'+str(x[1]+1) +'个词"'+ x[2]+ '"可能出现介词使用错误;\n'


    suggestion2 = ''
    for x in E2_list2:
        suggestion2 += '第'+str(x[0]+1)+'句句子:\n'+ sentence[x[0]] +'\n可能出现介词遗漏错误;\n'


    #score = '您的最后分数为: ' + str(Final_score)


    return suggestion,suggestion2









if __name__ == '__main__':



    Dict = dict_initialization()
    regr, clf1, clf2 = classifier_initialization()
    tokenizer = Sc.WordPunctTokenizer()
    essay = input_initialization()
    vectorizer_ALL = Fe.Vectorizer_initialization()








    sentence,tokens,sentence_tokens,pos_tag_list,TOKEN_list,POS_list = basic_statistic(essay)
    print POS_list



    Final_score,E1_list, E2_list, E2_list1, E2_list2 = Scoring_feature_extraction(tokens,Dict,sentence,pos_tag_list,TOKEN_list,POS_list,
                                                                                  regr, clf1, clf2, vectorizer_ALL)
    print printer(E2_list,E2_list1,E2_list2,Final_score)

    print Main.error_printer2(E1_list,sentence_tokens)



