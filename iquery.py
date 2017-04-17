import requests
import json
import re
import TrainCollection
import urllib.parse
import urllib.request
from city import city
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


def queryTickets():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'
    r = requests.get(url, verify=False)
    stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', r.text)
    diction2 = dict(stations)

    # 需要输入的参数
    date = input("请输入出发日期(yyyy-mm-dd):")
    start = input("请输入出发站:")
    end = input("请输入到达站:")
    print(date+' '+start+' 到 '+end)

    # 获取车站代码
    startcode = ''
    endcode = ''
    if diction2.__contains__(start):
        startcode = diction2.get(start)
    else:
        print("查询不到出发站")

    if diction2.__contains__(end):
        endcode = diction2.get(end)
    else:
        print("查询不到到达站")

    # 查票链接
    url = "https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}".format(date, startcode, endcode)
    r = requests.get(url, verify=False)
    rows = r.json()['data']['datas']
    trains = TrainCollection.TrainCollection(rows)
    trains.pretty_print()

def queryWeather():
    cityname = input('输入你想要查询的城市:')
    citycode = city.get(cityname)

    # 调用查询接口
    if citycode:
        try:
            url = 'http://www.weather.com.cn/data/cityinfo/%s.html' % citycode
            content = urllib.request.urlopen(url).read().decode('utf-8')
            # 把json转换成字典格式
            data = json.loads(content)
            result = data['weatherinfo']
            str_temp = ('天气:%s\n温度:%s~%s') % (result['weather'], result['temp1'], result['temp2'])
            print(str_temp)

            # 保留查询记录，当前时间、城市、天气
            #f = open('天气查询记录.txt', 'a')
            #f.write(('%s\n%s\n%s\n') % (time.strftime('%Y-%m-%d', time.localtime(time.time())), cityname, str_temp))
            #f.close()
        except:
            print('查询失败！')

    else:
        print('没有找到您输入的城市！')

if __name__ == '__main__':
    while True:
        kind = input('请输入想查询的对象(按Q退出):')
        if kind=="tickets":
            queryTickets()
        if kind=="weather":
            queryWeather()
        if kind=="Q":
            break
