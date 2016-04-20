# -*- coding: utf-8-*-
__author__ = 'apple'


import nltk
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from nltk.tokenize import WordPunctTokenizer
import nltk.data

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

def both_tokenizer(sentence_list):
    tokenizer = WordPunctTokenizer()
    sentence_tokens=[]
    for sentence in sentence_list:
        sentence_tokens.append(tokenizer.tokenize(sentence))
    return sentence_tokens


def mapping(word_offset,sentence_tokens):
    index = 0
    flag = len(sentence_tokens[index])
    while flag <= word_offset:
        index+=1
        flag += len(sentence_tokens[index])

    return index, len(sentence_tokens[index])-flag+word_offset
