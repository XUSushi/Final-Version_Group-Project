# -*- coding: utf-8 -*-

"""
Created on Mon Jun 25 21:22:27 2018

@author: 许逸文、朱纯慧
"""
import http.client  
import hashlib  
import json  
import urllib  
import random  

class Translation:
    """    
    @整合类：许逸文
	@function: 机器翻译模块；包含5个函数
    """	
    
    def __init__(self,number):
        """
    	@author: 许逸文
    	@function：初始化
        """
        self.number=number

	
    def test(self,string):
		
        """
    	@author:许逸文	@function:检查收到的字符串是否符合百度翻译api的要求，即是否小于等于6000字节。
    	@input param:传入的是语音识别模块用户修改后/识别出的字符串string
    	@return:输出的是判断结果，如果flag=0则超出限制，flag=1则符合要求。
    	"""        

        a=len(string)
        #判断字符串长度是否超过6000
        if a<=6000:
		 #如果小于等于6000则flag=1
            flag=1
            print("已成功接收数据，请稍候片刻...")
            print()
            
        else:
            flag=0
		#如果小于等于6000则flag=0
            print("您好，字符串长度超出限制，请重试！")      
        return(flag)
		
		
    def error_setting(i,id_list,key_list, fromLang, toLang, content):
        """
        @author:许逸文
        @function:差错处理。用于当翻译id和key失效时，自动无痕调用列表中的id和key，在系统中不会让用户看出来id和key失效的情况。
		 @place:在baidu_translate()函数里调用，放在差错处理“except Exception as e: ”中
		 @param:传入的是id和key列表中的第几项、id列表、key列表、源语言、译语言、待翻译的内容
		 @param:输出翻译后的结果
        """
       
		#里面不需要调用test()函数，因为在baidu_translate()函数运行到差错处理之前已经验证完了
        pp=id_list[i]
        kk=key_list[i]
		#根据输入的i来索引列表中的id和key
        qq = content
        saltt = random.randint(32768, 65536)  
        signn = pp + qq + str(saltt) + kk 
        #拼接起来
                
        signn = hashlib.md5(signn.encode()).hexdigest()
		
        myurll = '/api/trans/vip/translate'  + '?appid=' + pp + '&q=' + urllib.parse.quote(  
        qq) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(saltt) + '&sign=' + signn
        httpClientt = http.client.HTTPConnection('api.fanyi.baidu.com')  
        httpClientt.request('GET', myurll)  
                    # response是HTTPResponse对象  
        responses = httpClientt.getresponse()  
        jsonResponses = responses.read().decode("utf-8")
		# 获得返回的结果，结果为json格式
                        
                        
       
        jss = json.loads(jsonResponses)  # 将json格式的结果转换字典结构  
       
        dss = str(jss["trans_result"][0]["dst"])  # 取得翻译后的文本结果  
        return (dss); # 返回翻译结果                   
        
    def baidu_translate(self,id_list,key_list,content, fromLang, toLang):
        """
		@author: 朱纯慧
        @function: 调用百度翻译API，解析百度翻译结果，并呈现出译文
        
        Args:
            appid：字符串类型，百度翻译 APP ID
            secretKey：字符串类型，百度翻译API密钥
            myurl：百度翻译API HTTP地址
            salt：随机数
            q：原文内容
            sign：签名，拼接 appid+q+salt+密钥字符串
            dst：翻译后的文本结果
        Returns：
			返回dst，字符串类型   
        """
		
        a=0
    #    appid = '20180527000167630'  #APP ID
    #    secretKey = 'ct2Zql2XnOFkrmNptBiF'  #密钥
        appid=id_list[a]
        secretKey = key_list[a]
        httpClient = None  
        myurl = '/api/trans/vip/translate' 
        q = content	#传入要翻译的内容 
    	
        salt = random.randint(32768,65536)  #生成随机数
        sign = appid + q + str(salt) + secretKey  
        sign = hashlib.md5(sign.encode()).hexdigest()  
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(  
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(  
            salt) + '&sign=' + sign  #拼接url
        
        try:  
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')  
            httpClient.request('GET', myurl)  #请求HTTP响应
            response = httpClient.getresponse()  
            jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
            js = json.loads(jsonResponse)# 将json格式的结果转换字典结构  
            dst = str(js["trans_result"][0]["dst"]) # 取得翻译后的文本结果  
            return (dst);
            
        except Exception as e:  
		#@author：许逸文
		#@function: 异常处理，出现异常则存储API id和key的列表序号后移一位，使用新的id和密钥，调用百度翻译获得翻译内容
      
            i=a+1
			#id和key列表的序号后移一位
            b=Translation.error_setting(i,id_list,key_list, fromLang, toLang, content)
			#调用error_setting()函数，得到翻译结果b
            return (b);
			#返回结果
        finally:  
            if httpClient:  
                httpClient.close()  
    
    
    def revise_or_not(self,content):
        """
        @author: 朱纯慧
		 @function: 判断用户是否要修改译文，获取修改后的译文内容
        
        Args:
            ifrevise：接收用户输入的数字1或2
            afterContent：接收用户输入的修改后的内容
        
        Returns：
            返回afterContent，字符串类型
        """
        text=content
        while True:
            print ("是否修改译文？")
            print ("1. 是")
            print ("2. 否")
            ifrevise = input()
            if ifrevise == '1':
                print ("请输入修改后的内容：")
                afterContent = input()
                break
            elif ifrevise == '2':
                afterContent = text
                print()
                break
            else:
                print ("请输入数字1-2")
        return (afterContent);

