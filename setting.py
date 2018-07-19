# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 21:03:16 2018

@author: 许逸文、朱纯慧
"""
class Setting:
#@function:设定源语言和译语言

    def __init__(self,name):    
        self.name = name 
        
    def from_lang(self):
        """
        @author: 许逸文、朱纯慧
        @function: 用户选择源语言
                   通过输入数字1-5来选择语言，输入q可以直接退出程序
                   输入其他字符将重新选择源语言
        @Args:  flag：int 型，用来标记用户是否输入q以结束程序，flag = 1的时候程序结束
                fro：字符串，接收用户输入的内容
                fromLangdict：字典，由数字序号和符合百度机器翻译API要求的源语言名称组成键值对。
                inputLangdict：字典，由数字序号和符合bing语音识别API要求的源语言名称组成键值对。
        @output param: fromLang：字符串型，代表不同语言，方便后面的程序传给百度机器翻译API
                       flag：int 型，用来标记用户是否输入q以结束程序，flag = 1的时候程序结束
                       input_lang: 字符串型，代表不同语言，方便后面的程序传给bing语音识别API
    
        """
        while True:
            print ("请选择源语言，如果退出请输入q：") 
            print ("1. 中文")
            print ("2. 英文") 
            print ("3. 日语")  
            print ("4. 法语")  
            print ("5. 西班牙语")
            flag = 0
            fro = input()
            fromLang = ''
            input_lang=''
            fromLangdict={'1':'zh','2':'en','3':'jp','4':'fra','5':'spa'}
            inputLangdict={'1':'zh-CN','2':'en-US','3':'ja-JP','4':'fr-FR','5':'es-ES'}
            # #可在日后继续增加可选语言
            if fro =='q':
                flag=1
                break
            elif fro=='1' or fro=='2' or fro=='3' or fro=='4' or fro=='5':
                fromLang=fromLangdict[fro]
                input_lang=inputLangdict[fro]
                break
                """
                听取老师建议，用字典取代原来众多的if,elif，提升了效率，为日后增加更多语言提供便利
                """
            else:
                print ("请输入数字1-5")
                #防止因用户输错而出错的情况
    
        return fromLang,flag,input_lang


    def to_lang(self):
        """
        @author: 许逸文、朱纯慧
        @function: 用户选择译文语言
                   通过输入数字1-5来选择语言
                   输入其他字符将重新选择译文语言
        @Args: to：字符串，接收用户输入的内容
               toLang：字符串型，代表不同语言
               toLangdict:字典，由数字序号和译语言名称组成键值对。
    
        @output param: toLang，字符串类型，代表译语言名称
        """
        while True:
            print ("请选择译文语言：")  
            print ("1. 中文")
            print ("2. 英文")  
            print ("3. 日语")  
            print ("4. 法语")  
            print ("5. 西班牙语")
            to = input()
            toLang = ''
            toLangdict={'1':'zh','2':'en','3':'jp','4':'fra','5':'spa'}
            #可在日后继续增加可选语言
            if to=='1' or to=='2' or to=='3' or to=='4' or to=='5':
                toLang=toLangdict[to]
                break
                """
                听取老师建议，用字典取代原来众多的if,elif，提升了效率，为日后增加更多语言提供便利
                """
            else:
                print ("请输入数字1-5")
        return toLang