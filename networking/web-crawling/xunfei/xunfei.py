"""
###### CREATOR          Ted
###### DESCRIPTION      Xunfei TTS API
###### VERSION          v1.2
###### UPDATE           2018/12/24
"""
import json
import time
import base64
import logging
import hashlib
import urllib.request
from urllib.parse import urlencode


def init_logging():
    logging.basicConfig(format='[ %(asctime)s ] : %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


class XunfeiTTS:

    tts_api_url = 'http://api.xfyun.cn/v1/service/v1/tts'
    x_param = {
        'aue': 'lame',  # output mp3
        'auf': 'audio/L16;rate=16000',
        'voice_name': 'xiaoyan',
        'engine_type': 'intp65'
    }

    def __init__(self, app_id, api_key):
        self.app_id = app_id
        self.api_key = api_key

    def _assemble_http_header(self):
        """
        根据讯飞TTS说明来组装HTTP请求头
        :return:
        """
        current_time = str(int(time.time()))

        x_param_base64 = base64.b64encode(json.dumps(self.x_param).encode())

        m2 = hashlib.md5()
        m2.update(self.api_key.encode() + current_time.encode() + x_param_base64)
        x_checksum = m2.hexdigest()

        header = {
            'X-CurTime': current_time,
            'X-Param': x_param_base64,
            'X-Appid': self.app_id,
            'X-CheckSum': x_checksum,
            'X-Real-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }
        return header

    def text2speech(self, text, output_sound):
        """
        文本转语音
        :param text: 需要转换的文本
        :param output_sound: 转换完成后保存语音的文件
        """
        data = urlencode({'text': text}).encode('ascii')
        request = urllib.request.Request(self.tts_api_url, headers=self._assemble_http_header(),
                                         data=data, method='POST')
        response = urllib.request.urlopen(request)

        content_type = response.getheader('Content-Type')
        logging.info("Content-Type:{0}".format(content_type))
        if content_type == 'audio/mpeg':
            with open(output_sound, 'wb') as f:
                f.write(response.read())
            logging.info("Save sound to '{0}'".format(output_sound))
        else:
            logging.warning(response.read().decode())
