# -*- coding: utf-8-*-
__author__ = 'apple'


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import nltk
from nltk.tokenize import RegexpTokenizer
#from nltk.tokenize import PunktWordTokenizer
from nltk.tokenize import WordPunctTokenizer
import nltk.data
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import words

from nltk.stem import WordNetLemmatizer
import enchant

import copy

from nltk.chunk import RegexpParser
import pickle
import cPickle

all_prep = set(['of','in','for','on','with','at','by',
                'from','up','about','into','over','after','under','above','behind',
                'against','without','as','until','before','ago','across','through','off','toward','below'])
simi_prep = set(['in','by','on','at'])

words850_list = words.words('en-basic')

def sentence_tokenize(sentence):
    token = tokenizer.tokenize(sentence)
    if token[-1][-1] == '.':
        token[-1] = token[-1][:-1]
        token.append('.')

    return token



ignore_pos = set(['DT','JJ','PRP$'])




chunker = RegexpParser(r'''
NN:
{<NN.*>(<DT>|<JJ>|<PRP\$>)*(<NN.*>|<PRP>)}
VN:
{<VB.*>(<DT>|<JJ>|<PRP\$>)*(<NN.*>|<PRP>)}
''')


def initialization2():

    f = open('vectorizer/vectorizer_ALL.pkl','r')
    vectorizer_ALL = cPickle.load(f)

    return vectorizer_ALL


def initialization():

    f = open('vectorizer/vectorizer_LEMMA.pkl','r')

    vectorizer_LEMMA = cPickle.load(f)



    return vectorizer_LEMMA








def bigram_extractor(POS_list, num, mod):    #('apple','NN'), index






    sign_NNL = False
    sign_NNR = False
    sign_VNL = False


    NNL = NNL_lemma = NNL_POS = VNL = VNL_lemma = VNL_POS = '#'


    for index in range(num-1,-1,-1):
        if POS_list[index][1] in ignore_pos:
            continue

        elif POS_list[index][1][:2] == 'NN' and not sign_NNL:
            NNL_lemma = lemmatizer.lemmatize(POS_list[index][0],pos='n')
            NNL = POS_list[index][0]
            NNL_POS = POS_list[index][1]
            sign_NNL = True
            break

        elif POS_list[index][1][:2] == 'VB' and not sign_VNL:
            VNL_lemma = lemmatizer.lemmatize(POS_list[index][0],pos='v')
            VNL_POS = POS_list[index][1]
            VNL = POS_list[index][0]
            sign_VNL = True
            break



    NNR = NNR_POS = NNR_lemma ='#'


    if mod == 2:
        start = num+1
    else:
        start = num

    for index in range(start,len(POS_list)):
        if POS_list[index][1] in ignore_pos:
            continue

        elif POS_list[index][1][:2] == 'NN' or POS_list[index][1] =='PRP' and not sign_NNR:
            NNR = lemmatizer.lemmatize(POS_list[index][0],pos='n')
            NNR_lemma = lemmatizer.lemmatize(POS_list[index][0],pos='n')
            NNR_POS = POS_list[index][1]
            sign_NNR = True
            break

    if sign_NNL:

        return ({'PhraseL': NNL,'PhraseR': NNR, 'Phrase_lemmaL': NNL_lemma,'Phrase_lemmaR':NNR_lemma ,         #测试
              'Phrase_POS': (NNL_POS, NNR_POS)}, 'False')   #F2

    else:
        return ({'PhraseL': VNL,'PhraseR': NNR, 'Phrase_lemmaL':VNL_lemma ,'Phrase_lemmaR': NNR_lemma,         #测试
              'Phrase_POS': (VNL_POS, NNR_POS )}, 'False')   #F2




def words_inspector(word):
    d1 = enchant.Dict('en_GB')
    d2 = enchant.Dict('en_US')
    d3 = enchant.Dict('en_AU')



    if word not in [',','!','\'','"',":",'?']:
        if d1.check(word) == False and d2.check(word)==False and d3.check(word)== False:
            return False
    return True



def chunker(POS_list):

    result_list = []
    resultL_list = []
    resultPOS_list = []

    temp1 = '#'
    temp1L = '#'
    temp1POS = '#'


    temp2 = '#'
    temp2L = '#'
    temp2POS = '#'


    mod = 0  #啥也没遇到

    for x in POS_list:
        if mod == 0:   #什么都没找到
            if x[1][:2] == 'NN':
                temp1 =  x[0].lower()
                temp1L = lemmatizer.lemmatize(x[0],pos='n').lower()
                temp1POS = x[1]
                mod =1

            elif x[1][:2] == 'VB':
                temp1 = x[0].lower()
                temp1L = lemmatizer.lemmatize(x[0],pos='v').lower()
                temp1POS = x[1]
                mod = 2


        elif mod == 1:    #找到一个N的情况下
            if x[1][:2] == 'NN' or x[1][:3] == 'PRP' :
                temp2 =  x[0].lower()
                temp2L = lemmatizer.lemmatize(x[0],pos='n').lower()
                temp2POS = x[1]

                result_list.append((temp1,temp2))
                resultL_list.append((temp1L,temp2L))
                resultPOS_list.append((temp1POS,temp2POS))
                if x[1][:2] == 'NN':

                    temp1 = temp2
                    temp1L = temp2L
                    temp1POS = temp2POS


                    temp2 = '#'
                    temp2L = '#'
                    temp2POS = '#'

                else:
                    mod =0

                    temp1 = '#'
                    temp1L = '#'
                    temp1POS = '#'


                    temp2 = '#'
                    temp2L = '#'
                    temp2POS = '#'


            elif x[1][:2] == 'VB':
                temp2 =  x[0].lower()
                temp2L = lemmatizer.lemmatize(x[0],pos='v').lower()
                temp2POS = x[1]

                result_list.append((temp1,temp2))
                resultL_list.append((temp1L,temp2L))
                resultPOS_list.append((temp1POS,temp2POS))
                mod =2

                temp1 = temp2
                temp1L = temp2L
                temp1POS = temp2POS


                temp2 = '#'
                temp2L = '#'
                temp2POS = '#'

            elif x[1] =='IN':
                temp1 = '#'
                temp1L = '#'
                temp1POS = '#'


                temp2 = '#'
                temp2L = '#'
                temp2POS = '#'
                mod =0





        elif mod == 2:  #找到一个动词情况下：
            if x[1][:2] == 'NN' or x[1][:3] == 'PRP':
                temp2 =  x[0].lower()
                temp2L = lemmatizer.lemmatize(x[0],pos='n').lower()
                temp2POS = x[1]

                result_list.append((temp1,temp2))
                resultL_list.append((temp1L,temp2L))
                resultPOS_list.append((temp1POS,temp2POS))
                if x[1][:2] == 'NN':

                    temp1 = temp2
                    temp1L = temp2L
                    temp1POS = temp2POS


                    temp2 = '#'
                    temp2L = '#'
                    temp2POS = '#'
                    mod =1

                else:
                    mod =0

                    temp1 = '#'
                    temp1L = '#'
                    temp1POS = '#'


                    temp2 = '#'
                    temp2L = '#'
                    temp2POS = '#'

            elif x[1][:2] == 'VB':
                temp1 =  x[0].lower()
                temp1L = lemmatizer.lemmatize(x[0],pos='v').lower()
                temp1POS = x[1]

                mod =2

            elif x[1] =='IN':
                temp1 = '#'
                temp1L = '#'
                temp1POS = '#'


                temp2 = '#'
                temp2L = '#'
                temp2POS = '#'
                mod =0

    return result_list,resultL_list,resultPOS_list





def accuracy_calc(list1,list2):
    if len(list1)!=len(list2):
        print 'list1 not equal to list2!'
        return -1

    num1 = 0
    num2 = 0
    for index in range(len(list1)):
        if list1[index] == list2[index]:
            num1+=1
        if abs(list1[index]-list2[index])<1:
            num2+=1

    return num1*1.0/len(list1),num2*1.0/len(list2)




'''
def feature_extractor(POS_list,NUM):
    result_list,resultL_list,resultPOS_list = chunker(POS_list)
    L = [0]*len(DL)
    R = [0]*len(DR)
    L_L = [0]*len(DL_L)
    L_R = [0]*len(DL_R)
    POS = [0]*len(DPOS)
    for x in result_list:
        for y in range(len(DL)):
            if x[0] == DL[y]:
                L[y] =1
        for y in range(len(DR)):
            if x[1] == DR[y]:
                R[y] =1
    for x in resultL_list:
        for y in range(len(DL_L)):
            if x[1] == DL_L[y]:
                L_L[y] = 1
        for y in range(len(DL_R)):
            if x[1] == DL_R[y]:
                L_R[y] = 1

    for x in resultPOS_list:
        for y in range(len(DPOS)):
            if x == DPOS[y]:
                POS[y] =1


    if NUM:
        flag = 'False'
    else:
        flag = 'True'

    return ({'PhraseL': L,'PhraseR': R, 'Phrase_lemmaL':L_L ,'Phrase_lemmaR': L_R,
              'Phrase_POS': POS}, flag)

'''


def feature_extractor(POS_list,NUM):

    result_list,resultL_list,resultPOS_list = chunker(POS_list)

    Dall = []
    DPOS = []
    string_x = ''
    string_y = ''

    for x,y in result_list:
        string_x+=x + ' '
        string_y+=y + ' '



    string_x = ''
    string_y = ''

    for x,y in resultL_list:
        string_x+=x + ' '
        string_y+=y + ' '
    DL_L.append(string_x)
    DL_R.append(string_y)
    '''
    string_x = ''
    for x,y in resultPOS_list:
        string_x += x+y +' '
    DPOS.append(string_x)

    '''


    L = vectorizer.transform(DL)#.toarray()[0])
    R = vectorizer.transform(DR)#.toarray()[0])
    L_L = vectorizer_lemma.transform(DL_L)#.toarray()[0])
    L_R = vectorizer_lemma.transform(DL_R)#.toarray()[0])
    #POS = vectorizer_POS.transform(DPOS)#.toarray()[0])

    if NUM:
        flag = 'False'
    else:
        flag = 'True'

    return ({'PhraseL': L,'PhraseR': R, 'Phrase_lemmaL':L_L ,'Phrase_lemmaR': L_R }, flag)



def feature_extractor2(POS_list,NUM):
    result_list,resultL_list,resultPOS_list = chunker(POS_list)


    DL_LR = []
    D_LR = []
    DPOS = []
    DALL = []
    string_x = ''

    for x,y in result_list:
        string_x+=x + ' '+y +' '

    #D_LR.append(string_x)



    for x,y in resultL_list:
        string_x+=x + ' '+ y +' '

    #DL_LR.append(string_x)




    for x,y in resultPOS_list:
        string_x += x+y +' '

    #DPOS.append(string_x)
    DALL.append(string_x)

    '''

    string_x = ''
    string_y = ''

    for x,y in resultL_list:
        string_x+=x + ' '
        string_y+=y + ' '
    DL_L.append(string_x)
    DL_R.append(string_y)

    string_x = ''
    for x,y in resultPOS_list:
        string_x += x+y +' '
    DPOS.append(string_x)




    L = vectorizer.transform(DL)#.toarray()[0])
    R = vectorizer.transform(DR)#.toarray()[0])
    L_L = vectorizer_lemma.transform(DL_L)#.toarray()[0])
    L_R = vectorizer_lemma.transform(DL_R)#.toarray()[0])
    POS = vectorizer_POS.transform(DPOS)#.toarray()[0])
    '''

    #LR = vectorizer.transform(D_LR)#.toarray()[0])
    #L_LR = vectorizer_LEMMA.transform(DL_LR)
    #POS = vectorizer_POS.transform(DPOS)
    ALL = vectorizer_ALL.transform(DALL)
    if NUM:
        flag = 'False'
    else:
        flag = 'True'

    return ({'PhraseLRLemma': ALL}, flag)






def feature_extractor_Bigram(sentence,NUM):

    BOW = vectorizer.transform([sentence])


    if NUM:
        flag = 'False'
    else:
        flag = 'True'

    return ({'BOW': BOW}, flag)





if __name__ == '__main__':

    file = open("wiki_all_edited.txt",'r')
    #file = open("rural_all_edited.txt",'r')
    #file = open("test.txt",'r')
    #vectorizer_DL,vectorizer_DR,vectorizer_DL_L,vectorizer_DL_R,vectorizer_POS = initialization()
    #vectorizer_LEMMA = initialization()
    vectorizer_ALL = initialization2()
    tokenizer = WordPunctTokenizer()
    lemmatizer = WordNetLemmatizer()

    feature_set = []
    feature_set_bi = []
    num = 0
    count = 1
    error = []

    list_L = []
    list_R = []
    listL_L = []
    listL_R = []
    listPOS = []

    tokens_list = []


    while 1:

        lines = file.readlines(1000000)
        if not lines:
            break
        for line in lines:

            line = line.decode('utf-8','ignore')
            if line.strip() == '':
                continue

            #print line




            line = line.split('#@')
            a = int(line[2])
            if a not in [0,2,3]:
                continue



            tokens = sentence_tokenize(line[0])

            if len(tokens)<3:
                continue
            '''
            result1 = feature_extractor_Bigram(line[0],a)
            feature_set_bi.append(result1)
            #print result1
            '''
            POS_list = nltk.pos_tag(tokens)

            '''
            result_list,resultL_list,resultPOS_list = chunker(POS_list)

            for x in result_list:
                #if words_inspector(x[0]) and words_inspector(x[1]):
                    list_L.append(x[0])
                    list_R.append(x[1])

            for x in resultL_list:
                #if words_inspector(x[0]) and words_inspector(x[1]):
                    listL_L.append(x[0])
                    listL_R.append(x[1])
            for x in resultPOS_list:
                listPOS.append(x)


            '''





            result = feature_extractor2(POS_list,a)
            #result = feature_extractor_Bigram(tokens_list,a)
            #print result
            feature_set.append(result)

            count+=1
            print count


            #print result1,result2,result3

    '''
    print set(list_L)
    print set(list_R)
    print set(listL_L)

    print set(listL_R)
    print set(listPOS)
    '''
    #dic = [list(set(list_L)),list(set(list_R)),list(set(listL_L)),list(set(listL_R)),list(set(listPOS))]
    #dic = list(set(tokens_list))




    #print error


    f3 = open('testfile/cla1_feature_(LRLEMMAPOS)(300K).pkl','w')
    cPickle.dump(feature_set,f3,0)


    '''
    f3 = open('cla2_feature_0.5_(bi).pkl','w')
    cPickle.dump(feature_set_bi,f3,0)

    '''

