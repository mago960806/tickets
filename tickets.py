#coding=utf-8
"""程序名称：火车票查询器
Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快车
    -z          直达

Example:
    tickets 南昌 杭州东 2018-03-24
    tickets -dg 杭州东 南昌 2018-03-24
"""
import requests
from docopt import docopt
from stations import stations
from prettytable import PrettyTable
#构造一个类来解析数据
class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 高级软卧 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains,available_place, options):
        """查询的火车班次集合
        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.available_place = available_place
        self.options = options

    @property
    def trains(self):
        for raw_train in self.available_trains:
            raw_train_list = raw_train.split('|')
            train_no = raw_train_list[3]
            initial = train_no[0].lower()
            duration = raw_train_list[10]
            if not self.options or initial in self.options:
                train = [
                    train_no,# train number
                    '\n'.join([self.available_place[raw_train_list[6]],#始发站
                               self.available_place[raw_train_list[7]]]),#终点站
                    '\n'.join([raw_train_list[8],# 发车时间
                               raw_train_list[9]]),# 到站时间
                    duration,#时长
                    raw_train_list[-6] if raw_train_list[-6] else '--',# 一等 
                    raw_train_list[-7] if raw_train_list[-7] else '--',# 二等 
                    raw_train_list[-15] if raw_train_list[-15] else '--',# 高级软卧
                    raw_train_list[-8] if raw_train_list[-8] else '--',#  软卧
                    raw_train_list[-14] if raw_train_list[-14] else '--',#硬卧
                    raw_train_list[-11] if raw_train_list[-11] else '--',#硬座
                    raw_train_list[-9] if raw_train_list[-9] else '--',#无座
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)
def cli():
    arguments = docopt(__doc__)
    """
    stations.py是字典,通过parse_station.py生成的.通过get方法访问字典中对应的value.
    """
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    #忽略requests库访问HTTPS时的InsecureRequestWarning问题
    requests.packages.urllib3.disable_warnings()
    #通过format函数格式化url请求
    url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
    'leftTicketDTO.train_date={}&'
    'leftTicketDTO.from_station={}&'
    'leftTicketDTO.to_station={}&purpose_codes=ADULT').format(date, from_station, to_station)
    #发送请求并禁用SSL证书验证
    response = requests.get(url, verify=False)
    #调用requests内置的json解释器将结果保存为json格式
    available_trains = response.json()['data']['result']
    available_place = response.json()['data']['map']
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    TrainsCollection(available_trains,available_place,options).pretty_print()
if __name__=='__main__':
    cli()