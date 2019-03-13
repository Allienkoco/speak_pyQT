# -*- coding: utf-8 -*-

import sys
import json
from playsound import playsound
import threading
import time
import os
from gettoken import fetch_token

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode


class getsounds:
    # # fliepath 文件路径
    # filepath = os.getcwd()+os.sep+'text.txt'
    # # token
    # token = fetch_token()
    # # 要合成的文本信息
    # TEXT = '欢迎使用koco语音助手'
    # # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
    # PER = 4
    # # 语速，取值0-15，默认为5中语速
    # SPD = 6
    # # 音调，取值0-15，默认为5中语调
    # PIT = 15
    # # 音量，取值0-9，默认为5中音量
    # VOL = 5
    # # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    # AUE = 3

    def __init__(self, filepath, token, TEXT, PER, SPD, PIT, VOL):

        # fliepath 文件路径
        self.filepath = filepath
        # token
        self.token = token
    # 要合成的文本信息
        self.TEXT = TEXT
        # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        self.PER = PER
        # 语速，取值0-15，默认为5中语速
        self.SPD = SPD
        # 音调，取值0-15，默认为5中语调
        self.PIT = PIT
        # 音量，取值0-9，默认为5中音量
        self.VOL = VOL
        # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
        self.AUE = 3
    # 主函数

    def mainmsg(self):
        FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
        FORMAT = FORMATS[self.AUE]

        CUID = "123456PYTHON"

        TTS_URL = 'http://tsn.baidu.com/text2audio'
        #token = fetch_token()
        tex = quote_plus(self.TEXT)  # 此处TEXT需要两次urlencode
        print(tex)  # 打印需要输出的语言
        params = {'tok': self.token, 'tex': tex, 'per': self.PER, 'spd': self.SPD, 'pit': self.PIT, 'vol': self.VOL, 'aue': self.AUE, 'cuid': CUID,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

        data = urlencode(params)  # 格式化参数
        print('获取语音的网址:' + TTS_URL + '?' + data)

        req = Request(TTS_URL, data.encode('utf-8'))

        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()

            has_error = ('Content-Type' not in f.headers.keys()
                         or f.headers['Content-Type'].find('audio/') < 0)
        except URLError as err:
            print('asr http响应http代码 : ' + str(err.code))
            result_str = err.read()
            has_error = True

        save_file = self.filepath+'.txt' if has_error else self.filepath+'.'+ FORMAT
        with open(save_file, 'wb') as of:
            of.write(result_str)

        if has_error:
            if (IS_PY3):
                result_str = str(result_str, 'utf-8')
            print("tts api 错误:" + result_str)

        print("结果保存为 :" + save_file)
        # 播放文件
        # plsond=playsound('result.mp3')
        # print(plsond)
        return save_file
