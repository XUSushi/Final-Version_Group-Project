# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:41:44 2018

@author: 许逸文、李怡凡
@function:多语言语音翻译系统主程序。接收用户的语音wav文件，调用语音识别、机器翻译和语音合成(伪)模块，
          并给用户修改语音识别结果和机器翻译结果的选择，最后生成语音合成结果。

      
"""

from os import path
#基于微软必应语音识别
global BING_KEY
BING_KEY = "a0d5d94569064571ac331900a3a61f47"
#因为bing语音识别有7天权限，故设计出全局变量。过期后方便修改
global input_lang

from translation import Translation
from recognize import Recognize
from setting import Setting
from speech import Speech
#从其他脚本中引入设置类(Setting)，语音识别类(Recognize)，机器翻译类(Translation)和语音合成类(Speech)
if __name__ == '__main__':
    rec_obj=Recognize('语音识别')
    set_obj=Setting('设置')
    trans_obj= Translation("翻译")
    speech_obj=Speech('语音合成')
    #创建四个类的对象
    id_list=['20170601000049695','20170601000049695','20180529000169010','20180527000167630'];
    key_list=["ggOxjP2r4I9SsWRDF2ozO","gOxjP2r4I9SsWRDF2ozO","opRustpMgAtMC18WVtlR","ct2Zql2XnOFkrmNptBiF"];        
    #百度翻译API的id和key列表    
    '''
    正确的id_list为id_list=['20170601000049695','20170601000049695','20180529000169010','20180527000167630'];
         key_list为key_list=["gOxjP2r4I9SsWRDF2ozO","gOxjP2r4I9SsWRDF2ozO","opRustpMgAtMC18WVtlR","ct2Zql2XnOFkrmNptBiF"];        
         
    可故意让id和key出错的，测试异常处理功能
    '''
    
    while True:
        fromLang,flag1,input_lang=set_obj.from_lang()
        #接收源语言
        
        if flag1 == 1: 
            #判断用户是否在第一步选择源语言时就输入了‘q’，即退出程序
            break
        else:
            recognize_result=''
            content=''
            toLang = set_obj.to_lang()
            #接收译语言
            print("请输入您的文件路径：")
            filepath=input()
            #接收用户的文件路径输入
            #用于测试的两个文件的路径为：data/resource_en.wav 和 data/resource_fr.wav
            print("您的指令已接收！请稍等片刻~:)")
            rec_obj.denoise(filepath)
            #进行降噪处理，在这个函数在会识别用户输入的路径是否存在，如果不存在则请用户重新输入
            rec_obj.slice()
            #进行分片处理
            for i in range(0,1000):
                filename = "data/cache/output" + str(i)+ ".wav"
                if path.exists(filename):
                    recognize_result=rec_obj.bing_recognition(filename,input_lang)
                else:
                    break
                #调用Recognize类中的bing_recognition函数，用bing语音识别API对分好的每一片进行语音识别
            
            content=recognize_result
            print()
            print("语音识别结果为：\n",content)
            print()
            #向用户输出语音识别结果
            xiugai = rec_obj.revise_or_not(content)
            #调用Recognize类中的revise_or_not()函数接收用户的修改，如果有修改则返回修改后的，没有修改则仍为原来的值
            if xiugai == content:  
                   #xiugai = content 意味着用户没有修改的情况
                   print("未修改~")  
                   flag=trans_obj.test(content)
                   #将语音识别结果传给Translation类中的test()函数测试是否符合百度机翻API要求
                   #符合要求则flag=1,不符合则flag=0
                   if flag==1:
                       #flag=1意味着符合百度翻译API的要求
                       a=trans_obj.baidu_translate(id_list,key_list,content, fromLang, toLang)
                       #调用Translation类中的baidu_translate()函数进行翻译
                       print("机翻结果为：\n",a)
                       print()
                       #向用户显示机翻结果
                       content2 = trans_obj.revise_or_not(a)
                       #调用TranslaTion类中的revise_or_not()函数接收用户的修改，如果有修改则返回修改后的，没有修改直接传给下一步
                       if content2 == a:  
                       #content2=a意味着用户没有修改机翻结果    
					   
                           print("未修改~")  
                           speech_obj.text_speech(a)
                           print()
                           #调用Speech类（伪）中的text_speech()函数，向用户显示合成结果
                           print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                           continue
							
                       elif content2 != a:
                       #content2!=a意味着用户修改了机翻结果      
                           print("修改成功！\n",content2)
                           speech_obj.text_speech(a)
                           #调用Speech类（伪）中的text_speech()函数，向用户显示合成结果
                           print("-*"*19)
                           continue
                       
                   elif flag==0:
                        #flag=0意味着不符合百度翻译API的要求
                       print("您的语音长度超出限制，请重新输入语音！")
                       continue
                    
            elif xiugai != content:
                    #xiugai ！= content 意味着用户修改了语音识别结果
                    print("修改成功！\n")   
                    
                    flag=trans_obj.test(xiugai)
                    #将用户修改后的结果传给Translation类中的test()函数测试是否符合百度机翻API要求
                    #符合要求则flag=1,不符合则flag=0
                    if flag==1:
                        ##flag=1意味着符合百度翻译API的要求
                        a=trans_obj.baidu_translate(id_list,key_list,xiugai, fromLang, toLang)
                        #调用Translation类中的baidu_translate()函数进行翻译        
                        print("机翻结果为：\n",a)
                        print()
                        #向用户显示机翻结果
                        content2 = trans_obj.revise_or_not(a)
                        #调用TranslaTion类中的revise_or_not()函数接收用户的修改
                        #如果有修改则返回修改后的，没有修改直接传给下一步
                        if content2 == a:  
    					   #content2=a意味着用户没有修改机翻结果  
                            print()
                            print("未修改~\n")  
                            speech_obj.text_speech(a)
                            #调用Speech类（伪）中的text_speech()函数，向用户显示合成结果
                            print("-*"*19)
                            continue
                        elif content2 != a:
                            print()
                            print("修改成功！\n") 
                            print()
                            speech_obj.text_speech(a)
                            #调用Speech类（伪）中的text_speech()函数，向用户显示合成结果
                            print("-*"*19)
                    else:
                        #flag=0意味着不符合百度翻译API的要求
                        print("您的语音长度超出限制，请重新输入语音！")
                        continue
						

            