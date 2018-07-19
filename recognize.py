# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:08:47 2018

@author: 李怡凡、岳圣雅、许逸文
"""
#需要提前用pip安装pydub、speechRecognition
from pydub import AudioSegment
from os import path
# 基于微软必应语音识别
import speech_recognition as sr
# .wav的音频和本脚本应放在同一目录下
import numpy as np
import os
import wave
import nextpow2
import math
global BING_KEY
BING_KEY = "a0d5d94569064571ac331900a3a61f47"
#"a414e67c491b443fbe88d1c8f1fa9a5a"  
#a0d5d94569064571ac331900a3a61f47
global recognize_str
recognize_str=""
# 微软必应语音识别的key(32位)
# 由于微软有7天限制，每次key不一样，做成全局变量


#语音识别类
class Recognize:
    
    def __init__(self,name):    
        self.name = name 
    
    """
	def get_wave_filename(fileFullName):
	
		@author: 陈思明
		@function: 文件处理 
		# MP3文件转换成wav文件  
		# 判断文件后缀
		# 若为mp3，直接处理为16k采样率的wav文件；  	#若为wav，判断文件的采样率，不是8k或者16k的，直接处理为16k的采样率的wav文件  
		# 若为其他情况，返回AudioSegment处理  
		
		fileSufix = fileFullName[fileFullName.rfind('.')+1:]  
		print(fileSufix)  
		filePath = fileFullName[:fileFullName.find(os.sep)+1]  
		print(filePath)  
		if fileSufix.lower() == "mp3":  
			wavFile = "wav_%s.wav" %datetime.datetime.now().strftime('%Y%m%d%H%M%S')  
			wavFile = filePath + wavFile  
			cmdLine = "ffmpeg -i \"%s\" -ar 16000 " %fileFullName  
			cmdLine = cmdLine + "\"%s\"" %wavFile  
			print(cmdLine)  
			ret = subprocess.run(cmdLine)  
			print("ret code:%i" %ret.returncode)  
			return wavFile  
			#if ret.returncode == 1:  
			#   return wavFile  
			#else:  
			#   return None  
		else:  
			return fileFullName  
	# 文件处理为Wav，采样率16k的文件，返回文件名
	
    """
	
    def slice(self):
        """
		 @author:李怡凡
		 @description:音频切分
		 @input_file:input.wav
		 @output_file:output[i].wav
		 """
        path = 'data/cache'
        if os.listdir(path):
            for i in os.listdir(path):
                path_file = os.path.join(path,i)
                os.remove(path_file)
        sound_new = AudioSegment.from_file("data/input.wav", format="wav")
        #打开目标音频文件
        len_sound = len(sound_new) 
        #计算音频时长
        for i in range(0,1000):
            filename = "data/cache/output"+str(i)+".wav"
            #命名输出文件名
            n=i+1
            sound_new[15000*i:15000*n].export(filename, format="wav")
            #每7秒一切分，并按顺序输出
            if len_sound<15000:
                break
            #当音频文件小于7秒时停止切分
            len_sound=len_sound-15000
    
    def bing_recognition(self,filename,input_language):
        """
		 @author:岳圣雅
        @description bing语音识别API调用函数
        @param string filename  读入的文件名
        @param string input_language  语言
        @return recognize_str 识别的字符串
        """
        global BING_KEY
        global recognize_str
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)
        # text.wav可以换成切片好之后的音频名称
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  #读取分片后的音频文件
    
        try:
            #print("Bing recognition results:")
            #print(r.recognize_bing(audio, key=BING_KEY, show_all=True))
            dict1 = r.recognize_bing(audio, key=BING_KEY, language= input_language, show_all=True)
            str1 = dict1['DisplayText']
            recognize_str=recognize_str+str1 #此处的str1即识别结果，可以直接拿出来，用于下一阶段的自主文字修改
        except sr.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
        
        return recognize_str
            
    def berouti1(SNR):
        # @description: 幅度谱函数
        if -5.0 <= SNR <= 20.0:
            a = 3 - SNR * 2 / 20
        else:
            if SNR < -5.0:
                a = 4
            if SNR > 20:
                a = 1
        return a
        
    def berouti(SNR):
        # @description:功率谱函数
        if -5.0 <= SNR <= 20.0:
            a = 4 - SNR * 3 / 20
        else:
            if SNR < -5.0:
                a = 5
            if SNR > 20:
                a = 1
        return a
            
    def find_index(x_list):
        index_list = []
        for i in range(len(x_list)):
            if x_list[i] < 0:
                index_list.append(i)
        return index_list
    
    def denoise(self,audio):
        """
        @author:李怡凡
        @description:音频降噪
        @input_file:语音路径
        @output_file:input.wav
        """
        """
        @语音文件路径差错处理体系：如用户输入的文件地址无效，则告知用户并重新接收用户输入
        @author:许逸文
        """
        try:
            fpath=audio
            ff = wave.open(fpath)
        except Exception as es:
            print("输入的文件地址不存在！请重新输入~")
            fpath=input()
            while True:
                if path.exists(fpath):
                    print()
                    print("文件地址已收到，请稍候片刻...")
                    break
                else:
                    print("出错了！请重新输入~注意大小写哦！")
                    fpath=input()
            #若文件路径不存在，则一直提示用户，直到正确
        finally:
            # 读取格式信息
            # (nchannels, sampwidth, framerate, nframes, comptype, compname)
            f = wave.open(fpath)            
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            fs = framerate
            # 读取波形数据
            str_data = f.readframes(nframes)
            f.close()
            # 将波形数据转换为数组
            x = np.fromstring(str_data, dtype=np.short)
            # 计算参数
            len_ = 20 * fs // 1000
            PERC = 50
            len1 = len_ * PERC // 100
            len2 = len_ - len1
            # 设置默认参数
            Thres = 3
            Expnt = 2.0
            beta = 0.002
            G = 0.9
            # 初始化汉明窗
            win = np.hamming(len_)
            #重叠的归一化增益+ 增加50％重叠
            winGain = len2 / sum(win)
        
            #噪声幅度计算-假设前5帧是噪声/静音
            nFFT = 2 * 2 ** (nextpow2.nextpow2(len_))
            noise_mean = np.zeros(nFFT)
    
            j = 0
            for k in range(1, 6):
                noise_mean = noise_mean + abs(np.fft.fft(win * x[j:j + len_], nFFT))
                j = j + len_
                noise_mu = noise_mean / 5
            k = 1
            img = 1j
            x_old = np.zeros(len1)
            Nframes = len(x) // len2 - 1
            xfinal = np.zeros(Nframes * len2)
    
            for n in range(0, Nframes):
                # Windowing
                insign = win * x[k-1:k + len_ - 1]
                # 计算帧的傅里叶变换
                spec = np.fft.fft(insign, nFFT)
                # 计算幅度
                sig = abs(spec)
    
                # 保存嘈杂的相位信息
                theta = np.angle(spec)
                SNRseg = 10 * np.log10(np.linalg.norm(sig, 2) ** 2 / np.linalg.norm(noise_mu, 2) ** 2)
    
        
    
    
                if Expnt == 1.0:  # 幅度谱
                    alpha = Recognize.berouti1(SNRseg)
                    
                else:  # 功率谱
                    alpha = Recognize.berouti(SNRseg)
                    #############
                sub_speech = sig ** Expnt - alpha * noise_mu ** Expnt;
                # 当纯净信号小于噪声信号的功率时
                diffw = sub_speech - beta * noise_mu ** Expnt
                # beta负面组件
    
    
                z = Recognize.find_index(diffw)
                if len(z) > 0:
                    # 用估计出来的噪声信号表示下限值
                    sub_speech[z] = beta * noise_mu[z] ** Expnt
                    if SNRseg < Thres:  # 更新噪声频谱
                        noise_temp = G * noise_mu ** Expnt + (1 - G) * sig ** Expnt  # 平滑处理噪声功率谱
                        noise_mu = noise_temp ** (1 / Expnt)  # 新的噪声幅度谱
                    # flipud函数实现矩阵的上下翻转，是以矩阵的“水平中线”为对称轴
                    # 交换上下对称元素
                    sub_speech[nFFT // 2 + 1:nFFT] = np.flipud(sub_speech[1:nFFT // 2])
                    x_phase = (sub_speech ** (1 / Expnt)) * (np.array([math.cos(x) for x in theta]) + img * (np.array([math.sin(x) for x in theta])))
    
                    xi = np.fft.ifft(x_phase).real
                    # --- Overlap and add ---------------
                    xfinal[k-1:k + len2 - 1] = x_old + xi[0:len1]
                    x_old = xi[0 + len1:len_]
                    k = k + len2
            # 保存文件
            wf = wave.open('data/input.wav', 'wb')
            # 设置参数
            wf.setparams(params)
            # 设置波形文件 .tostring()将array转换为data
            wave_data = (winGain * xfinal).astype(np.short)
            wf.writeframes(wave_data.tostring())
            wf.close()

    def revise_or_not(self,content):
        """
		 @author:许逸文
		 @description:用户修改bing语音识别的结果
		 @input param:语音识别后的内容（字符串）
		 @output param:用户修改后的结果（字符串）
		"""
       
        while True:
            print ("是否修改识别结果？")
            print ("1. 是")
            print ("2. 否")
			#给用户提供是否修改的选项
            ifrevise = input()
			#接收用户的输入
            if ifrevise == '1':
                print ("请输入修改后的内容：")
                afterContent = input()
				#用户选择修改，则将用户修改赋给 afterContent
                break
            elif ifrevise == '2':
                afterContent = content 
                #用户选择不修改，则将bing语音识别的结果（content）赋给afterContent
                print()
                break
            else:
                print ("请输入数字1-2")
        return (afterContent)
		#返回afterContent值



    
    