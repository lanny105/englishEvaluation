#coding:utf-8
#from django.shortcuts import render
#from django.template import loader, Context
from django.shortcuts import render_to_response
#from datetime import datetime
#from django.http import HttpRequest
#from django.template.context_processors import csrf
#import os

from learn.English import LR_scoring_engine as LR
import random
#from learn.English import
# Create your views here.

string2 = "</span>"

def add_style(string):
    string1 = "<p style=\"text-align: justify;\"><span style=\"font-size: 14pt; font-family: 'book antiqua', palatino, serif;\">"
    string2 = "</span></p>"

    return string1 + string + string2


def add_underline(sentence_string):

    string1 = "<span style=\"color: #ff0000; text-decoration: underline;\">"
    #string2 = "</span>"

    return string1 + sentence_string + string2


def add_spelling(tokens):
    string1 = "<span style=\"color: #ffff00; background-color: #0000ff;\">"
    #string2 = "</span>"

    return string1 + tokens + string2

def add_preposition(tokens):
    string1 = "<span style=\"color: #00ff00; background-color: #ff0000;\">"

    return string1 + tokens + string2



def highlight(sentence_tokens, E1_list, E2_list1, E2_list2):

    newsentence = []


    for x in E1_list:
        sentence_tokens[x[0]][x[1]]  = add_spelling(sentence_tokens[x[0]][x[1]])



    for x in E2_list1:
        #suggestion += '第'+str(x[0]+1)+'句句子第'+str(x[1]+1) +'个词 '+ x[2]+ ' 可能出现介词使用错误;\n'
        sentence_tokens[x[0]][x[1]]  = add_preposition(sentence_tokens[x[0]][x[1]])


    for x in sentence_tokens:
        string2 = ''
        for y in range(len(x)-1):
            string2 += x[y]
            if x[y+1] not in ['\'',',',':','?','!','']:
                    string2 +=' '
        string2 =string2 + x[-1] +" "
        newsentence.append(string2)





    for x in E2_list2:
        #suggestion2 += '第'+str(x[0]+1)+'句句子可能出现介词遗漏错误;\n'
        newsentence[x[0]] = add_underline(newsentence[x[0]])


    result = ""
    for x in newsentence:
        result += x

    #print result


    result = add_style(result)

    return result













'''
def index(request):
    t = loader.get_template('index.html')
    C = Context({})

    return HttpResponse(t.render(C))
'''


#   base = /Users/apple/Desktop/django_file/mysite

'''
def index(req):
    #strings = LR.getdir()

    f = open('static/example_essay/example001.txt','r')
    all_the_text = f.read()
    strings = all_the_text.decode('utf-8')
    f.close()


    return render_to_response('index副本.html', {'strings':strings})





'''


'''



def index(request):


    if request.method == 'POST' and u'for example' in request.POST:  #获得用户输入值



        #books = Book.objects.filter(title__icontains=q) #调用model文件中的Book类方法处理后返回结果
        #strings = str(request.POST)
        a = random.randint(1,5)
        file_name = 'static/example_essay/example00'+str(a)+'.txt'
        f = open(file_name)
        all_the_text = f.read()
        strings = all_the_text.decode('utf-8')
        f.close()


        return render_to_response('index副本.html', #渲染输出模板
            {'strings':strings,'a':strings,'score':0})




    elif request.method == 'POST' and u'display' in request.POST:
        #a = float(request.POST['display'])
        strings = str(request.POST['display'])
        #a +=.5
        sentence,tokens,sentence_tokens,pos_tag_list,TOKEN_list,POS_list,strings = LR.basic_statistic(strings)

        Final_score,E1_list, E2_list, E2_list1, E2_list2 = LR.Scoring_feature_extraction2(tokens,sentence,pos_tag_list,
                                                                                          TOKEN_list,POS_list)

        suggestion3 = LR.Main.error_printer2(E1_list,sentence_tokens)
        suggestion, suggestion2 = LR.printer(E2_list,E2_list1,E2_list2,Final_score)
        suggestion = suggestion +suggestion2
        suggestion = suggestion.strip()
        return render_to_response('index副本.html', #渲染输出模板
            {'strings':strings,'score':Final_score, 'feedback': {'E1_list':suggestion3,'E2_list1': E2_list1, 'E2_list2':E2_list2,
                                                                 'E2_list':suggestion}})


    else:

        return render_to_response('index副本.html', #渲染输出模板
                    {'strings':'','score':0})


'''


def index(request):


    if request.method == 'POST' and u'for example' in request.POST:  #获得用户输入值



        #books = Book.objects.filter(title__icontains=q) #调用model文件中的Book类方法处理后返回结果
        #strings = str(request.POST)
        a = random.randint(1,5)
        file_name = 'static/example_essay/example00'+str(a)+'.txt'
        f = open(file_name)
        all_the_text = f.read()
        strings = all_the_text.decode('utf-8','ignore')
        f.close()

        strings = add_style(strings)

        return render_to_response('index.html', #渲染输出模板
            {'strings':strings,'score':0.0})




    elif request.method == 'POST' and u'display' in request.POST:
        #a = float(request.POST['display'])
        strings = str(request.POST['display'])
        strings = strings.decode('utf-8','ignore')
        strings = LR.replace(strings)
        #print strings

        #a +=.5
        sentence,tokens,sentence_tokens,pos_tag_list,TOKEN_list,POS_list,strings = LR.basic_statistic(strings)
        Final_score,E1_list, E2_list, E2_list1, E2_list2 = LR.Scoring_feature_extraction2(tokens,sentence,pos_tag_list,
                                                                                          TOKEN_list,POS_list)

        suggestion3,E1_list = LR.Main.error_printer2(E1_list,sentence_tokens,sentence)


        strings = highlight(sentence_tokens, E1_list, E2_list1, E2_list2)
        suggestion, suggestion2 = LR.printer(E2_list,E2_list1,E2_list2,Final_score,sentence)
        suggestion = suggestion +suggestion2
        suggestion = suggestion.strip()

        if suggestion.strip() == '':
            suggestion = "您的作文没有出现介词错误，请保持^_^～"

        if suggestion3.strip() == '':
            suggestion3 = '您的作文没有出现拼写错误，请保持^_^～'
        
        return render_to_response('index.html', #渲染输出模板
            {'strings':strings,'score':Final_score, 'feedback': {'E1_list':suggestion3,#'E2_list1': E2_list1, 'E2_list2':E2_list2,
                                                                 'E2_list':suggestion}})


    else:

        return render_to_response('index.html', #渲染输出模板
                    {'strings':add_style(''),'score':0.0})


