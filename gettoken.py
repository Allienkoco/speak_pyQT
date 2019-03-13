# -*- coding: utf-8 -*-

import sys
import json

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


"""  TOKEN start """
API_KEY = 'iSfygWuK7Go5a5ajtU53eQ39'
SECRET_KEY = 'MqsGiGc0WEZN5wkNpdTsiHMr2urhuwOy'
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选

#获取token
def fetch_token():
    print("获取 token 开始")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        result_str ='获取token网站错误代码 : ' + str(err.code)
        return('获取token网站错误代码 : ' + str(err.code))
    if (IS_PY3):
        result_str = result_str.decode()

    print('返回的json',result_str)
    result = json.loads(result_str)
    print('编码后的json',result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            return('范围不正确')
        print('获取的access_token: %s ; 获取的expires_in: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        return ('可能API_KEY或SECRET_KEY不正确:在令牌响应中没有找到access_token或范围')


"""  TOKEN end """