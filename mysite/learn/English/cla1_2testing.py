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
#from nltk.tokenize import PunktWordTokenizer
import nltk.data
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import re
import copy
from nltk.tag.sequential import ClassifierBasedPOSTagger
from nltk.corpus import treebank

from collections import OrderedDict

import pickle
from sklearn import linear_model as linear_model
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn import tree
from sklearn.svm import SVR
from sklearn.naive_bayes import MultinomialNB
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC

import cPickle
from sklearn.metrics import precision_recall_curve


def classifier_initialization():
    f = open('MAXENT_prep_classifier_new.pkl','r')
    #f = open('NB_prep_classifier_F1.pkl','r')
    CLF1 = cPickle.load(f)


    f = open('classifier2/linearSVC.pkl','r')
    CLF2 = cPickle.load(f)

    return CLF1,CLF2


def classifier(feature):

    if feature[0] == []:
        result1 = 'True'
    else:
        result1 = CLF1.classify(feature[0])



    result2 = CLF2.predict(feature[1])

    if result1 == 'True' and result2 == 'True':
        return 'True'
    else:
        return 'False'

def combination(result1,result2):
    result = []
    if len(result1)!=len(result2):
        raise AttributeError('list1 not equal to list2!')

    for x in range(len(result1)):
        if result1[x] == 'True' and result2[x] == 'True':
            result.append('True')
        else:
            result.append('False')

    return result


'''
def feature_extractor():
    pass

'''
def initialization():

    f=open('testfile/cla1&2_feature_0.5_(LRLEMMAPOS)(rural).pkl','r')
    Y = cPickle.load(f)


    #random.shuffle(Y)
    #Y = Y[:]
    #temp = copy.deepcopy(Y)
    Y2 = []
    tags = []
    result = []
    num = 1
    for x in range(len(Y)):
        for key in Y[x][1]:
            features = (Y[x][0],(list(Y[x][1][key].toarray()[0])))
            tags.append(Y[x][2])
            result.append(classifier(features))

        print num
        num+=1
    print PRF1_calc(result,tags)
    print accuracy_calc(result,tags)

    return ''

def initialization2():

    f=open('testfile/cla1&2_feature_0.5_(LRLEMMAPOS)(new!).pkl','r')
    Y = cPickle.load(f)
    random.shuffle(Y)           #(feature1,feature2,flag)
    Y = Y
    temp = copy.deepcopy(Y)
    tags =[]



    class2 = []
    class1 = []
    num = 1
    for x in range(len(Y)):
        #features_set1.append(Y[0])
        tags.append(Y[x][2])
        class1.append((Y[x][0],Y[x][2]))

        for key in Y[x][1]:
            #features_set2.append()
            class2.append((list(temp[x][1][key].toarray()[0]),Y[x][2]))

        print num
        num+=1


    return class1,class2


def initialization3():

    f=open('testfile/cla1&2_feature_0.5_(BOW)(new!).pkl','r')
    Y = cPickle.load(f)
    random.shuffle(Y)           #(feature1,flag)
    temp = copy.deepcopy(Y)
    tags =[]



    class2 = []
    class1 = []
    num = 1
    for x in range(len(Y)):
        for key in Y[x][0]:
            class2.append((list(temp[x][0][key].toarray()[0]),Y[x][1]))

        print num
        num+=1


    return class2


def spliter(data_set):
    features = []
    tags = []

    for x in data_set:
        features.append(x[0])
        tags.append(x[1])

    return features,tags



def PRF1_calc(list1,list2):

    if len(list1)!=len(list2):
        raise AttributeError('list1 length not equal to list2!')

    num1 = num2 = num3 = 0
    for x in range(len(list1)):
        if list1[x] == 'False':
            num1 += 1
        if list2 [x] == 'False':
            num2 += 1
        if list1[x] == 'False' and list2[x] == 'False':
            num3 += 1

    #accuracy = num *1.0/len(list1)
    print num1,num2,num3,len(list1)
    if num1 ==0:
        precision = 0
    else:
        precision = num3*1.0/num1


    recall = num3*1.0/num2

    if (precision+recall) == 0:
        f1_score =0
    else:
        f1_score = 2*precision*recall/(precision+recall)

    return precision,recall,f1_score#,accuracy



def accuracy_calc(list1,list2):
    if len(list1)!=len(list2):
        print 'list1 not equal to list2!'
        return -1

    num1 = 0
    for index in range(len(list1)):
        if list1[index] == list2[index]:
            num1+=1

    return num1*1.0/len(list1)




def cross_valid(X,Y,k_fold):

    #print X

    kf =cross_validation.KFold(len(X),n_folds=k_fold)

    accuracy_rate = 0

    precision_rate = 0

    recall_rate = 0

    f1_score_rate = 0
    num = 1


    for train_index, test_index in kf:

        train = []
        test = []
        train2 = []
        test2 = []

        for item in train_index:
            train.append(X[item])
            train2.append(Y[item])
        for item in test_index:
            test.append(X[item])
            test2.append(Y[item])
        classifier = nltk.classify.NaiveBayesClassifier.train(train)
        #classifier2 = nltk.classify.MaxentClassifier.train(
        #                 train,max_iter=5)


        features,tags = spliter(train2)

        clf1 = LinearSVC()
        clf1.fit(features,tags)


        features_test,tags_test = spliter(test)
        features_test2, tags_test2 = spliter(test2)

        if tags_test!= tags_test2:
            raise AttributeError('tags_test not equal to tags_test2!')



        result1 = classifier.classify_many(features_test)

        result2 = clf1.predict(features_test2)

        result = combination(result1,result2)




        precision,recall,f1_score = PRF1_calc(result,tags_test)
        accuracy = accuracy_calc(result,tags_test)

        print '--------------------------------',num,'-------------------------'
        print accuracy,precision,recall,f1_score
        num+=1


        #
        # print result

        accuracy_rate += accuracy



        precision_rate += precision

        recall_rate += recall


        f1_score_rate += f1_score



    accuracy_rate = accuracy_rate*1.0/k_fold

    precision_rate = precision_rate*1.0/k_fold



    recall_rate = recall_rate*1.0/k_fold


    f1_score_rate = f1_score_rate*1.0/k_fold


    return accuracy_rate,precision_rate,recall_rate,f1_score_rate



def cross_valid_sklearn(A,k_fold):
    #print A
    X,Y = spliter(A)

    #print X
    #print Y

    if len(X)!=len(Y):
        print 'training set not equal to test set!'
        return -1
    kf =cross_validation.KFold(len(X),n_folds=k_fold)


    accuracy_rate = accuracy2_rate = accuracy3_rate = accuracy4_rate =  0
    precision_rate = precision2_rate = precision3_rate = precision4_rate  = 0
    recall_rate = recall2_rate = recall3_rate = recall4_rate  = 0
    f1_score_rate = f1_score2_rate = f1_score3_rate = f1_score4_rate  = 0


    num = 1

    for train_index, test_index in kf:
        train_X = []
        train_Y = []
        test_X = []
        test_Y = []

        for item in train_index:
            train_X.append(X[item])
            train_Y.append(Y[item])
        for item in test_index:
            test_X.append(X[item])
            test_Y.append(Y[item])



        clf = LinearSVC()                                       #0.66 0.302564102564 0.22433460076 0.257641921397
                                                                #0.737 0 0.0 0
                                                                #0.674 0.369294605809 0.338403041825 0.353174603175
                                                                #0.686 0.352601156069 0.231939163498 0.279816513761
        clf.fit(train_X,train_Y)
        result = clf.predict(test_X)



        accuracy = accuracy_calc(result,test_Y)



        precision,recall,f1_score = PRF1_calc(result,test_Y)



        print '-----',num,'------'
        num+=1
        print accuracy,precision,recall,f1_score




        #
        # print result

        accuracy_rate += accuracy




        precision_rate += precision

        recall_rate += recall

        f1_score_rate += f1_score



    accuracy_rate = accuracy_rate*1.0/k_fold

    precision_rate = precision_rate*1.0/k_fold


    recall_rate = recall_rate*1.0/k_fold


    f1_score_rate = f1_score_rate*1.0/k_fold








    return accuracy_rate,accuracy3_rate,accuracy4_rate,\
    precision_rate,precision3_rate,precision4_rate,\
    recall_rate,recall3_rate,recall4_rate,\
    f1_score_rate,f1_score3_rate,f1_score4_rate


if __name__ == '__main__':


    CLF1 ,CLF2 = classifier_initialization()
    #initialization()
    #X,Y = initialization2()
    A = initialization3()
    print cross_valid_sklearn(A,10)
    #print cross_valid(X,Y,10)

    '''                   53928条数据                                                        测试：
    (0.9424507373091479, 0.5334350994681899, 0.6812671959751592)   NB   +  linearSVC       (0.8474893162393162, 0.45899030811514535, 0.5954771511682462)
     ACCURACY 0.749533610902                                                                         0.658696856939



    (0.9321573414182778, 0.5828737443372071, 0.7172526623543847)   MAXENT + linearSVC       (0.8026900965397549, 0.5352234919716476, 0.6422217400737688)
     0.769399933285                                                                          0.673620457604
    自己训练 自己跑

    10-fold
    (0.6079059623961838, 0.909258756925888, 0.7286269779960162)     NB + linearSVC
    0.6608997967471846

    ( 0.6080921412285079, 0.9106821535342077, 0.7292271350510778)   MAX + linearSVC
    0.6614005076368367


    BOW   :     linearSVC

    0.5478019354965361,  0.4969721111445427  0.5211331801962962
    0.5416833781205487

    '''










