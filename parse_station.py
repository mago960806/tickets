import re
import requests
from pprint import pprint
#url为火车站点名称获取的接口
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050'
#忽略requests库访问HTTPS时的InsecureRequestWarning问题
requests.packages.urllib3.disable_warnings()
#发送请求并禁用SSL证书验证
response = requests.get(url, verify=False)
#使用正则替换字符串
"""
[\u4e00-\u9fa5]+
\u4e00是unicode表中的第一个汉字,\u9fa5是最后一个汉子。
即匹配所有汉字
[A-Z]+
即匹配所有大写字母
"""
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
#将数据类型转换为字典,并使用pprint格式化打印出来,缩进为4个空格
pprint(dict(stations), indent=4)