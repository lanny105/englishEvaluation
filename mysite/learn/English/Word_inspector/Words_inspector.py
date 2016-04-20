# -*- coding: utf-8-*-
__author__ = 'apple'


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import enchant
import os


basedir = str(os.getcwd())+ '/learn/English/Word_inspector/'

def words_inspector(list):
    d1 = enchant.Dict('en_GB')
    #d2 = enchant.Dict('en_US')
    d3 = enchant.Dict('en_AU')
    d2 = enchant.DictWithPWL('en_US', basedir + 'mywords.txt')
    error_suggestion = []

    for index in range(len(list)):
        word = list[index]
        if word not in [',','!','\'','"',":",'?']:
            if d1.check(word) == False and d2.check(word)==False and d3.check(word)== False:
                #print word

                item = [index,word]
                suggestion = d1.suggest(word)
                if len(suggestion)>3:
                    item.append(suggestion[:3])
                else:
                    item.append(suggestion)

                error_suggestion.append(item)
    return error_suggestion

