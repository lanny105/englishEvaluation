# -*- coding: utf-8-*-
__author__ = 'apple'


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import cPickle
import os


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()



all_prep = set(['of','in','for','on','with','at','by',
                'from','up','about','into','over','after','under','above','behind',
                'against','without','as','until','before','ago','across','through','off','toward','below'])

impossible = 'bubusddsudhudhusha'


basedir = str(os.getcwd())+ '/learn/English/'

def Vectorizer_initialization():

    f = open('vectorizer/vectorizer_ALL.pkl','r')
    vectorizer_ALL = cPickle.load(f)

    return vectorizer_ALL



def Vectorizer_initialization2():

    f = open(basedir+'vectorizer/vectorizer(ALL_newfeature_50k_5).pkl','r')   #>5
    vectorizer_ALL = cPickle.load(f)

    return vectorizer_ALL


def Vectorizer_initialization3():

    f = open('vectorizer/vectorizer(ALL_newfeature(Bobi)_(500k)_5).pkl','r')   #>5
    vectorizer_ALL = cPickle.load(f)

    return vectorizer_ALL



def Preposition_indexing(tokenlist):
    index = []
    for x in range(len(tokenlist)):
        if tokenlist[x] in all_prep:
            index.append(x)

    return index





def Preposition_usage1_extractor(POS_list, num):    #('apple','NN'), index

    if len(POS_list)<3:
        print 'sentence too short'
        return []


    if num == -1:
        return []

    '''           BIGRAM       '''

    if num >= len(POS_list):
        return []

    prep = POS_list[num][0].lower()
    if prep in all_prep:
        if num == 0:
            BGL = ('#',prep)
            BGR = (prep,POS_list[num+1][0].lower())
            BGL_POS = ('#','IN')
            BGR_POS = ('IN',POS_list[num+1][1])


        elif num == len(POS_list)-1:
            BGL = (POS_list[num-1][0].lower(),prep)
            BGR = (prep,'#')
            BGL_POS = (POS_list[num-1][1],'IN')
            BGR_POS = ('IN','#')


        else:
            BGL = (POS_list[num-1][0].lower(),prep)
            BGR = (prep,POS_list[num+1][0].lower())
            BGL_POS = (POS_list[num-1][1],'IN')
            BGR_POS = ('IN',POS_list[num+1][1])




    else:
        print 'index not right!',POS_list[num][0].lower(),num
        return ['index not right!']




    '''      PN_lemma                 '''



    lemmatizer = WordNetLemmatizer()


    sign_PNL = False
    sign_PV = False
    sign_DT = False
    sign_IN = False
    sign_PJ = False

    for index in range(num-1,-1,-1):
        if POS_list[index][1][:2] == 'NN' and not sign_PNL:
            PNL = (lemmatizer.lemmatize(POS_list[index][0],pos='n'), prep)
            sign_PNL = True
            break

        if POS_list[index][1][:2] == 'VB' and not sign_PV:
            PV = (POS_list[index][0], prep)
            PVL = (lemmatizer.lemmatize(POS_list[index][0],pos='v'), prep)
            PVPOS = (POS_list[index][1],'IN')
            sign_PV = True
            break

        if POS_list[index][1][:2] == 'DT' and not sign_DT:
            PDT = (POS_list[index][0], prep)
            sign_DT = True
            break

        if POS_list[index][1][:2] == 'IN' and not sign_IN:
            PIN = (POS_list[index][0], prep)
            sign_IN = True
            break

        if POS_list[index][1][:2] == 'JJ' and not sign_PJ:
            PJ = (prep, POS_list[index][0])
            sign_PJ = True
            break


    if not sign_PNL:
        PNL = ('#', prep)
    if not sign_PV:
        PV = ('#', prep)
        PVL = ('#', prep)
        PVPOS = ('#','IN')


    if not sign_DT:
        PDT = ('#', prep)

    if not sign_IN:
        PIN = ('#', prep)

    if not sign_PJ:
        PJ = ('#', prep)


    '''    trigram    '''

    NULL = ('#','#')
    POS_list.insert(0,NULL)
    POS_list.insert(0,NULL)
    POS_list.insert(-1,NULL)
    POS_list.insert(-1,NULL)

    if POS_list[num+2][0].lower() in all_prep:
        TGL = (POS_list[num][0].lower(),POS_list[num+1][0].lower(),POS_list[num+2][0].lower())
        TGR = (POS_list[num+2][0].lower(),POS_list[num+3][0].lower(),POS_list[num+4][0].lower())
        TGL_POS = (POS_list[num][1],POS_list[num+1][1],'IN')
        TGR_POS = ('IN',POS_list[num+3][1],POS_list[num+4][1])


    else:
        print 'index not right!'
        #print POS_list
        return ['index not right!']



    return  {'BGL': BGL, 'BGL_POS': BGL_POS, 'BGR': BGR, 'BGR_POS': BGR_POS,
              'PNL': PNL, 'PV':PV,'PVL': PVL, 'PVPOS': PVPOS, 'PDT': PDT,'PIN': PIN,
              'TGL': TGL, 'TGR': TGR, 'TGL_POS': TGL_POS, 'TGR_POS': TGR_POS}   #F1


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




def chunker2(POS_list):      #(NN,NN)  (NN,PRP)   (NN,VB)   (VB ,NN )  (JJ , VB) (JJ ,NN)  (JJ,PRP)  (VB, JJ) (NN,JJ)

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

            elif x[1][:2] == 'JJ':
                temp1 = x[0].lower()
                temp1L = x[0].lower()
                temp1POS = x[1]
                mod = 3


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

            elif x[1] == 'JJ':
                temp2 =  x[0].lower()
                temp2L = x[0].lower()
                temp2POS = x[1]

                result_list.append((temp1,temp2))
                resultL_list.append((temp1L,temp2L))
                resultPOS_list.append((temp1POS,temp2POS))
                mod =3

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

            elif x[1] == 'JJ':
                temp2 =  x[0].lower()
                temp2L = lemmatizer.lemmatize(x[0]).lower()
                temp2POS = x[1]

                result_list.append((temp1,temp2))
                resultL_list.append((temp1L,temp2L))
                resultPOS_list.append((temp1POS,temp2POS))

                temp1 = temp2
                temp1L = temp2L
                temp1POS = temp2POS


                temp2 = '#'
                temp2L = '#'
                temp2POS = '#'
                mod = 3


            elif x[1] =='IN':
                temp1 = '#'
                temp1L = '#'
                temp1POS = '#'


                temp2 = '#'
                temp2L = '#'
                temp2POS = '#'
                mod =0

        elif mod == 3:   #找到一个形容词

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
                    mod = 1

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




    return result_list,resultL_list,resultPOS_list






def preosition_usage2_extractor(POS_list, vectorizer_ALL):
    result_list,resultL_list,resultPOS_list = chunker(POS_list)
    print result_list,resultL_list,resultPOS_list

    DALL = []
    string_x = ''

    for x,y in result_list:
        string_x+=x + ' '+y +' '


    for x,y in resultL_list:
        string_x+=x + ' '+ y +' '


    for x,y in resultPOS_list:
        string_x += x+y +' '

    DALL.append(string_x)

    #ALL = list(vectorizer_ALL.transform(DALL).toarray()[0])
    ALL = vectorizer_ALL.transform(DALL)


    #return {'PhraseLRLemma': ALL}
    return ALL






def preosition_usage2_extractor2(POS_list, vectorizer_ALL):
    result_list,resultL_list,resultPOS_list = chunker2(POS_list)
    print result_list,resultL_list,resultPOS_list

    DALL = []
    string_x = ''

    for x,y in result_list:
        string_x+=x + ' '+y +' '+ impossible +' '


    for x,y in resultL_list:
        string_x+=x + ' '+ y +' ' + impossible +' '


    for x,y in resultPOS_list:
        string_x += x+y +' '

    DALL.append(string_x)

    ALL = vectorizer_ALL.transform(DALL)


    #return {'PhraseLRLemma': ALL}
    return ALL





def preosition_usage2_extractor3(raw_sentence, vectorizer_ALL):

    ALL = vectorizer_ALL.transform([raw_sentence])

    return  ALL