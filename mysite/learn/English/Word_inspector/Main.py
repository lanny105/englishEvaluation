# -*- coding: utf-8-*-
__author__ = 'apple'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import Tokenizer
import Words_inspector


def error_printer(error_suggestion,sentence_list):
    for item in error_suggestion:
        args = Tokenizer.mapping(item[0],sentence_list)
        print '第',args[0]+1,'句句子中第',args[1]+1,'个词',item[1],'出现拼写错误;'
        print '可能正确的词为:',
        num = 1
        for word in item[2]:
            print num, ')',word,
            num +=1
        print '\n'


def error_printer2(error_suggestion,sentence_list,sentence):
    suggestion = ''
    #print sentence_list
    #print error_suggestion
    E1_list = []
    for item in error_suggestion:
        args = Tokenizer.mapping(item[0],sentence_list)
        E1_list.append(args)
        suggestion+= '第'+str(args[0]+1)+'句句子:\n'+ sentence[args[0]]+'\n中第'+str(args[1]+1)+'个词"'+str(item[1])+'"可能出现拼写错误;\n'
        suggestion +='可能正确的词为:\n'
        num = 1
        for word in item[2]:
            suggestion+= str(num)+ ')'+ word +' '
            num +=1


        if num ==1:
            suggestion +="没有拼写建议。"
        suggestion+='\n'

    suggestion = suggestion.strip()

    return suggestion,E1_list


if __name__=='__main__':

    file_object = open('testessay')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )

    all_the_text = all_the_text.decode('utf-8', 'ignore')

    sentence = Tokenizer.sent_tokenizer(all_the_text)

    tokens = Tokenizer.word_tokenizer(all_the_text)
    sentence_tokens = Tokenizer.both_tokenizer(sentence)
    print sentence_tokens
    error_suggestion = Words_inspector.words_inspector(tokens)

    error_printer(error_suggestion,sentence_tokens)

