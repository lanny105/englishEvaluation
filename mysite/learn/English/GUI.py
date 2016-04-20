#coding=utf-8
__author__ = 'apple'

'''
本文件是关于GUI的构造

'''



import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import wx
import LR_scoring_engine as LR
import os


class TextFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'English Essay Grader',
                size=(960, 520), style = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX) )
        panel = wx.Panel(self, -1)
        self.multiLabel1 = wx.StaticText(panel, -1, "Write your essay here!",pos = (40,15))
        self.multiText1 = wx.TextCtrl(panel, -1,
               "",
               size=(550, 425), pos = (40,50) ,style=wx.TE_MULTILINE|wx.TE_RICH2) #创建一个多行文本控件
        self.multiText1.SetInsertionPoint(0) #设置光标插入点为首部

        self.button1 = wx.Button(panel,-1, label = 'Open', pos = (605, 50), size = (80, 20))
        self.button2 = wx.Button(panel,-1, label = 'About', pos = (605, 80), size = (80, 20))
        self.button3 = wx.Button(panel,-1, label = 'Clear', pos = (605, 110), size = (80, 20))






        self.button4 = wx.Button(panel,-1, label = 'Grading!', pos = (605, 170), size = (80, 20))
        #self.label3 = wx.StaticText(panel,-1, label = '-1ms', pos = (600, 160), size = (80, 20))  #-1ms 表示未触发分词



        self.multiLabel2 = wx.StaticText(panel, -1, "Score:",pos = (715,15))
        self.multiText2 = wx.TextCtrl(panel, -1,
               "Not started...",
               size=(205, 50), pos = (715,50) ,style=wx.TE_MULTILINE|wx.TE_READONLY) #创建一个多行文本控件
        self.multiText2.SetBackgroundColour('#EFEFEF')


        self.multiLabel3 = wx.StaticText(panel, -1, "Spelling Error:",pos = (715,115))
        self.multiText3 = wx.TextCtrl(panel, -1,
               "",
               size=(205, 75), pos = (715,150) ,style=wx.TE_MULTILINE|wx.TE_READONLY) #创建一个多行文本控件
        self.multiText3.SetBackgroundColour('#EFEFEF')


        self.multiLabel4 = wx.StaticText(panel, -1, "Preposition Error1:",pos = (715,240))
        self.multiText4 = wx.TextCtrl(panel, -1,
               "",
               size=(205, 75), pos = (715,275) ,style=wx.TE_MULTILINE|wx.TE_READONLY) #创建一个多行文本控件
        self.multiText4.SetBackgroundColour('#EFEFEF')

        self.multiLabel5 = wx.StaticText(panel, -1, "Preposition Error2:",pos = (715,365))
        self.multiText5 = wx.TextCtrl(panel, -1,
               "",
               size=(205, 75), pos = (715,400) ,style=wx.TE_MULTILINE) #创建一个多行文本控件
        self.multiText5.SetBackgroundColour('#EFEFEF')

        '''
        self.multiLabel6 = wx.StaticText(panel, -1, "Neighborhood matching:",pos = (50,390))
        self.multiText6 = wx.TextCtrl(panel, -1,
               "Please click on the segment button on the right...",
               size=(500, 50), pos = (50,410) ,style=wx.TE_MULTILINE|wx.TE_READONLY) #创建一个文本控件
        self.multiText6.SetBackgroundColour('#EFEFEF')

        self.button8 = wx.Button(panel,-1, label = 'Segment', pos = (575, 410), size = (80, 20))
        self.label5 = wx.StaticText(panel,-1, label = '-1ms', pos = (600, 440), size = (80, 20))

        self.multiLabel7 = wx.StaticText(panel, -1, "Shortest path matching:",pos = (50,460))
        self.multiText7 = wx.TextCtrl(panel, -1,
               "Please click on the segment button on the right...",
               size=(500, 50), pos = (50,480) ,style=wx.TE_MULTILINE|wx.TE_READONLY) #创建一个文本控件
        self.multiText7.SetBackgroundColour('#EFEFEF')

        self.button9 = wx.Button(panel,-1, label = 'Segment', pos = (575, 480), size = (80, 20))
        self.label6 = wx.StaticText(panel,-1, label = '-1ms', pos = (600, 510), size = (80, 20))


        '''
        '''
        成员函数和button控件绑定
        '''

        self.Bind(wx.EVT_BUTTON,self.OnButton1,self.button1)
        self.Bind(wx.EVT_BUTTON,self.OnButton2,self.button2)
        self.Bind(wx.EVT_BUTTON,self.OnButton3,self.button3)
        self.Bind(wx.EVT_BUTTON,self.OnButton4,self.button4)




        #initialization:
        self.filename = ""  #路径名



        self.Dict = LR.dict_initialization()
        #self.regr, self.clf1, self.clf2 = LR.classifier_initialization()
        self.regr, self.clf1, self.clf2 = LR.classifier_initialization2()
        #self.regr, self.clf1, self.clf2 = LR.classifier_initialization3()
        self.tokenizer = LR.Sc.WordPunctTokenizer()
        self.essay = ""
        #self.vectorizer_ALL = LR.Fe.Vectorizer_initialization()
        self.vectorizer_ALL = LR.Fe.Vectorizer_initialization2()
        #self.vectorizer_ALL = LR.Fe.Vectorizer_initialization3()




    def ReadFile(self):         #读取文本文件到文本框
        if self.filename:
            try:
                f = open(self.filename, 'r')
                all_the_text = f.read()
                chinese_string = all_the_text.decode('utf-8')
                f.close()
                self.multiText1.SetValue(chinese_string)
                self.multiText1.SetStyle(0,len(self.multiText1.GetValue())-1,(wx.TextAttr(colText= "black",colBack =wx.NullColour , font =wx.NullFont)))
            except:
                wx.MessageBox("%s is not a text file."
                              % self.filename, "error tip",
                              style = wx.OK | wx.ICON_EXCLAMATION)





    def OnButton1(self,event):
        '''
        打开开文件对话框
        '''
        file_wildcard = "All files(*.*)|*.*|Text files(*.txt)|*.txt|"
        dlg = wx.FileDialog(self, "Open text file...",
                            os.getcwd() +"/text_file/",
                            style = wx.OPEN,
                            wildcard = file_wildcard)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
        dlg.Destroy()



    def OnButton2(self,event):          #About信息对话框
        dlg=wx.MessageDialog(None,"Author：1152238 叶秋阳\n"
                                  "Email：1152238@tongji.edu.cn","About",wx.OK|wx.ICON_INFORMATION)
        result=dlg.ShowModal()
        dlg.Destroy()

    def OnButton3(self,event):
        self.multiText1.Clear()
        self.multiText2.Clear()
        self.multiText3.Clear()
        self.multiText4.Clear()
        self.multiText5.Clear()
        self.essay = ''






    '''
    OnButton4 - OnButton8为触发相应算法的函数，调用segmenter.py后，将文本信息和时间返回并显示在相应控件上

    '''
    def OnButton4(self,event):
        self.essay = LR.replace(self.multiText1.GetValue().decode('utf-8'))
        self.multiText1.SetStyle(0,len(self.essay)-1,(wx.TextAttr(colText= "black",colBack =wx.NullColour , font =wx.NullFont)))

        sentence,tokens,sentence_tokens,pos_tag_list,TOKEN_list,POS_list = LR.basic_statistic(self.essay)

        if sentence == 0:
            dlg=wx.MessageDialog(None,"Hi, try to write longer please～","Message",wx.OK|wx.ICON_EXCLAMATION)
            result=dlg.ShowModal()
            dlg.Destroy()
            return

        #Final_score,E1_list, E2_list, E2_list1, E2_list2 = LR.Scoring_feature_extraction(tokens,self.Dict,sentence,pos_tag_list,TOKEN_list,POS_list,
        #                                                                self.regr,self.clf1,self.clf2,self.vectorizer_ALL)
        Final_score,E1_list, E2_list, E2_list1, E2_list2 = LR.Scoring_feature_extraction2(tokens,self.Dict,sentence,pos_tag_list,TOKEN_list,POS_list,
                                                                        self.regr,self.clf1,self.clf2,self.vectorizer_ALL)


        #Final_score,E1_list, E2_list, E2_list1, E2_list2 = LR.Scoring_feature_extraction3(tokens,self.Dict,sentence,pos_tag_list,TOKEN_list,POS_list,
        #                                                                self.regr,self.clf1,self.clf2,self.vectorizer_ALL)
        suggestion,suggestion2,score = LR.printer(E2_list,E2_list1, E2_list2,Final_score)
        suggestion3 = LR.Main.error_printer2(E1_list,sentence_tokens)
        self.multiText2.SetValue(score)
        self.multiText3.SetValue(suggestion3)
        self.multiText4.SetValue(suggestion)
        self.multiText5.SetValue(suggestion2)
        points = self.multiText1.GetFont().GetPointSize()
        f = wx.Font(points, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT,underline=True, faceName="", encoding=wx.FONTENCODING_DEFAULT)

        self.multiText1.SetStyle(0,10,wx.TextAttr("blue", wx.NullColour, f))
        #self.token_string = result[0]





    '''
    def OnButton7(self,event):
        result = segmenter.RMINM_ALL(segmenter.preprocessing(self.multiText1.GetValue()),self.dict)
        self.multiText5.SetValue(result[0])
        a = result[1]/1000
        b = result[2]
        if b < 1:
            self.label4.SetLabelText(str(a)+'ms')
        else:
            self.label4.SetLabelText(str(b*1.0 + a*1.0/1000)+'s')

    def OnButton8(self,event):
        result = segmenter.NM_ALL(segmenter.preprocessing(self.multiText1.GetValue()),self.dict)
        self.multiText6.SetValue(result[0])
        a = result[1]/1000
        b = result[2]
        if b < 1:
            self.label5.SetLabelText(str(a)+'ms')
        else:
            self.label5.SetLabelText(str(b*1.0 + a*1.0/1000)+'s')

    def OnButton9(self,event):
        result = segmenter.SPM_ALL(segmenter.preprocessing(self.multiText1.GetValue()),self.dict)
        self.multiText7.SetValue(result[0])
        a = result[1]/1000
        b = result[2]
        if b < 1:
            self.label6.SetLabelText(str(a)+'ms')
        else:
            self.label6.SetLabelText(str(b*1.0 + a*1.0/1000)+'s')
    '''


if __name__ == '__main__':
    app = wx.App()
    frame = TextFrame()
    frame.Show()
    app.MainLoop()


