# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 22:21:17 2018

@author: 许逸文
"""

class Speech:
    """
    @function: 该类为伪语音合成类。用于接收机器翻译的结果，合成为语音，并最终输出语音文件。
    注：我小组负责的程序部分是“语音识别”和“机器翻译”模块
       为整个程序的流程和完整，故写出此伪语音合成类，模拟功能，并由小组成员录制了输出音频
    """
    def __init__(self,name):    
        self.name = name 
        
    def text_speech(self,text):
        """
        @function:接收机器翻译的文本并合成为语音输出到output文件夹
        """
        content=text
        #接收文本
        print("\n语音正在合成中...")
        print()
        print("已生成语音！快到 output 文件夹里查看吧~")
        print()