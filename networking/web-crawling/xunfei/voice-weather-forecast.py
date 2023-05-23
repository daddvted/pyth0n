"""
###### CREATOR          Ted
###### DESCRIPTION      Voice weather forecast
###### VERSION          v1.5
###### UPDATE           2018/06/20
"""
import re
import sys
import datetime
import logging
import urllib.request
import lxml.html

from xunfei import XunfeiTTS, init_logging


def get_weather_data():
    """
    通过中国天气网获取天气获取
    :return:
    {
        'status': 'success | error',
        'msg': '获取天气数据失败',
        'today': {
            'weather': '晴',
            'temperature': [13, 30]
        },
        'tomorrow': {
            'weather': '晴',
            'temperature': [14, 29]
        }
    }
    """

    chengdu_weather = 'http://www.weather.com.cn/weather/101270101.shtml'

    request = urllib.request.Request(chengdu_weather, method='GET')
    response = urllib.request.urlopen(request)

    weather_data = {}
    if response.status != 200:
        weather_data['status'] = 'error'
        weather_data['msg'] = '获取天气数据失败'
        return weather_data

    else:
        weather_data['status'] = 'success'
        today = {}
        tomorrow = {}

        # Parse weather today
        html = lxml.html.fromstring(response.read().decode())
        weather_today = html.xpath('.//input[@id="hidden_title"]')
        today_text = weather_today[0].attrib['value']
        weather = today_text.split()[2]

        temperature = []
        match = re.search('([0-9]+)/([0-9]+)', today_text)
        if match:
            temperature = list(match.groups())
            temperature.sort()

        today['weather'] = weather
        today['temperature'] = [int(x) for x in temperature]
        weather_data['today'] = today

        # Parse weather tomorrow

        weather_tomorrow = html.xpath('//div[@id="7d"]/ul/li')[1]
        weather = weather_tomorrow.xpath('./p[@class="wea"]/text()')[0]
        temperature_text = weather_tomorrow.xpath('./p[@class="tem"]')[0]
        temperature = re.findall('([0-9]+)', temperature_text.text_content(), re.M)
        temperature.sort()

        tomorrow['weather'] = weather
        tomorrow['temperature'] = temperature
        weather_data['tomorrow'] = tomorrow

        return weather_data


def get_aqi():
    aqi_url = "http://aqicn.org/city/chengdu/cn/"
    request = urllib.request.Request(aqi_url, method='GET')
    response = urllib.request.urlopen(request)
    print(response.read().decode())

    if response.status != 200:
        return ""
    else:
        html = lxml.html.fromstring(response.read().decode())
        aqiwgtinfo = html.xpath('//div[@id="aqiwgtinfo"]')[0].text_content()
        aqiwgtvalue = html.xpath('//div[@id="aqiwgtvalue"]')[0].text_content()
        print(aqiwgtinfo, aqiwgtvalue)
        return ", 实时空气质量指数, {}, {}".format(aqiwgtvalue, aqiwgtinfo)


def generate_speech(data, when):
    if data['status'] == 'error':
        speech = data['msg']
    else:
        weather = data[when]
        weather_tpl = '{0}，{1}到{2}°C'
        weather_text = weather_tpl.format(weather['weather'], *weather['temperature'])
        if when == 'today':

            today_tpl = '早上好，今天是{0}年{1}月{2}日,'
            now = datetime.datetime.now()
            today_text = today_tpl.format(now.year, now.month, now.day)
            speech = today_text + weather_text
        else:
            tomorrow_tpl = '晚上好，明天是{0}年{1}月{2}日,'
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            tomorrow_text = tomorrow_tpl.format(tomorrow.year, tomorrow.month, tomorrow.day)
            speech = tomorrow_text + weather_text
    return speech


if __name__ == '__main__':
    # 获取命令行参数： today, tomorrow
    # 生成不同的文本
    forecast = sys.argv[1]

    init_logging()

    tts_app_id = '5ace35fe'
    tts_api_key = '363430a6da9ad1087374ff781b063235'

    # 服务器上语音保存位置
    mp3 = '/usr/share/nginx/speech/weather-{0}.mp3'.format(forecast)
    # mp3 = 'weather.mp3'

    cd_weather = get_weather_data()
    cd_weather_speech = generate_speech(cd_weather, forecast)
    # aqi_speech = get_aqi()
    aqi_speech = ""
    weather_speech = cd_weather_speech + aqi_speech
    logging.info(weather_speech)
    tts = XunfeiTTS(tts_app_id, tts_api_key)
    tts.text2speech(weather_speech, mp3)
