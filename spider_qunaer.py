import concurrent.futures
import math
import threading
import requests
import json
import time
import subprocess
import random
from functools import partial
import redis
from urllib3.exceptions import InsecureRequestWarning
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")  # 编码
location = 'fake_useragent.json'
from fake_useragent import UserAgent
ua = UserAgent(cache_path=location)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 取消警告
t = int(round(time.time() * 1000))  # 获取时间戳
flights_data = {
    "result": [],
    "need": 0
}
# client = redis.Redis(host="localhost", port=6379, decode_responses=True, db=5)
# client = redis.Redis(host="10.0.1.130", port=63790, decode_responses=True, db=5, password="yun_4827")
ip_pool8 = redis.ConnectionPool(host='124.232.153.85', port=63799, db=int(8), max_connections=1000)
client8 = redis.Redis(connection_pool=ip_pool8, password="yun_4827", decode_responses=True)

ip_pool0 = redis.ConnectionPool(host='124.232.153.85', port=63799, db=int(0), max_connections=1000)
client0 = redis.Redis(connection_pool=ip_pool0, password="yun_4827", decode_responses=True)


# 获取cookie
def get_cookie():
    try:
        cookie_pool = client0.randomkey()  # 随机获取cookie
        print(cookie_pool)
        cookie_value = client0.hmget(cookie_pool, "cookie")
        if cookie_value == [None]:
            get_cookie()
        else:
            cookie_value = "".join(cookie_value[0].decode())
            client0.delete(cookie_pool)
        return {'data': cookie_value}
    except Exception as e:
        return {'error': f'get_cookie Error,{e}'}


# 三字码转换
def convert(code):
    headers = {
        "user-agent": str(ua.random)
    }
    url = "https://www.qunar.com/suggest/livesearch2.jsp"
    params = {
        "lang": "zh",
        "q": code,
        "sa": "true",
        "ver": "1"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 or response.status_code == 201:
            city_name = response.json()['result'][0]['key']
            return {'city_name': city_name}
        else:
            return {'error': f"状态码错误，{response.status_code}"}
    except Exception as e:
        return {'error': f"convert Error,{e}"}


def proxy_ip():
    while True:
        time.sleep(random.uniform(0.02, 0.04))
        try:
            key_name = client8.randomkey()
            cd_data_redis = client8.get(key_name)
            cd_data = str(cd_data_redis.decode())
            break
        except Exception as e:
            print('jiuyuan IP redis:%s' % str(e), flush=True)
    return str(cd_data)


# 获取数据


def get_data(start_data, cookie):
    global flights_data
    dep_air = convert(start_data['from'])
    arr_air = convert(start_data['to'])
    if dep_air.get('error') is None and arr_air.get('error') is None:
        url = "https://flight.qunar.com/touch/api/inter/wwwsearch"
        header = {
            "user-agent": str(ua.random),
            "cookie": str(cookie.get('data'))
        }
        params = {
            "depCity": dep_air['city_name'],  # 出发地
            "arrCity": arr_air['city_name'],  # 到达点
            "depDate": start_data['daytime'],  # 出发时间
            "adultNum": start_data['adt_num'],
            "childNum": 0,
            "from": "qunarindex",
            "ex_track": "",
            "es": "",
            "_v": 8,
        }
        if start_data.get('proxy') is None:
            pro_ip = 'null'
        else:
            pro_ip = str(start_data['proxy'])
        try:
            if pro_ip != 'null':
                response = requests.get(url=url, headers=header, params=params, verify=False,
                                    proxies={'http': 'http://' + str(pro_ip)}, timeout=18)
            else:
                response = requests.get(url=url, headers=header, params=params, verify=False,
                                    timeout=18)
            response.encoding = "utf-8"

            if response.status_code == 200 or response.status_code == 201:
                resp = json.loads(response.text)
                if resp['status'] != -1:  # 没票
                    if resp.get('code') != -1 or resp.get('code') is None and resp.get("['result']['flightPrices']") != {}: # 假数据
                        print(f"{pro_ip}请求成功")
                        return {'data': response.text}   # 成功
                    else:
                        print(resp)
                        return {'error': f"{pro_ip}出现假数据"}
                        # time.sleep(3)
                        #
                        # get_data(start_data, cookie)
                        # pass
                else:
                    print(resp)
                    return {'error': f"航班为空"}
                    # pass
            else:
                return {'error': f'状态码出错, {response.status_code}'}
        except Exception as e:
            return {'error': f'get_data Error,{e}'}
    else:
        return {'error': dep_air['error']+arr_air['error']}


def exec_data(data):
    try:
        flights = json.loads(data)['result']['flightPrices']
        for key, value in flights.items():
            flight_name = key  # 航班名称
            lowest_price = value['price']['lowPrice']  # 航班基础价格
            flight = value['journey']['trips'][0]['flightSegments'][0]
            stop_cities = ""    # 停靠点
            if value['journey']['nonStopTransferAirports'] != []:
                stop_cities = value['journey']['trips'][0]['transInfos'][0]['cityName']
                flight0 = value['journey']['trips'][0]['flightSegments'][0]
                flight1 = value['journey']['trips'][0]['flightSegments'][1]
                departure_name = flight0['depAirportCode']  # 航班出发点
                arr_name = flight1['arrAirportCode']  # 航班到达点
                departure_time = flight0['depDate'] + " " + flight['depTime']  # 航班出发时间
                departure_time = departure_time.replace("-", "").replace(":", "")
                departure_time = departure_time.replace(" ", "")
                arr_time = flight1['arrDate'] + " " + flight['arrTime']  # 航班到达时间
                arr_time = arr_time.replace(" ", "")
                arr_time = arr_time.replace("-", "").replace(":", "")

            else:
                stop_cities = ""
                departure_name = flight['depAirportCode']  # 航班出发点
                arr_name = flight['arrAirportCode']  # 航班到达点
                departure_time = flight['depDate'] + flight['depTime']  # 航班出发时间
                departure_time = departure_time.replace("-", "").replace(":", "")
                departure_time = departure_time.replace(" ", "")
                arr_time = flight['arrDate'] + flight['arrTime']  # 航班到达时间
                arr_time = arr_time.replace(" ", "")
                arr_time = arr_time.replace("-", "").replace(":", "")

            flight_seat = value['journey']['seatInfo']['nums']  # 座位信息
            cabin = value['price']['lowPriceBase']['cabin'] # 仓位信息
            flight_tax = value['price']['tax']  # 航班税
            total_price = value['price']['lowTotalPrice']  # 航班总价格
            flight_result = pares(flight_name, departure_name, departure_time, arr_name, arr_time, flight_seat, cabin, lowest_price, flight_tax, total_price, stop_cities)
            flights_data['result'].append(flight_result)
    except Exception as e:
        return {'error': f"exec_data Error,{e}"}


def pares(flightNumber, iataCode, dateTime, iataCode1, arrTime, set, cabinClass, base, taxTotal, amount, stops):
  list_flight = []
  flight_dict = {
    "flightNumber": flightNumber,
    "depAirport": iataCode,
    "depTime": ''.join(dateTime),
    "depTerminal": '',  # 登机楼
    "arrAirport": iataCode1,
    "arrTime": ''.join(arrTime),
    "arrTerminal": '',  # 登机楼
    "stopCities": stops,
    "operatingFlightNumber": '',
    "cabin": cabinClass,
    "cabinClass": "",
    "seats": set,
    "aircraftCode": "",
    "operating": 0  # 不是共享1是共享
  }
  list_flight.append(flight_dict)
  adultPrice = math.ceil(float(base))
  adultTax = math.ceil(float(taxTotal))
  adultTotalPrice = amount
  mongo_dict = {
    '_id': 'Qunargj' + '-' + str(list_flight[0]['depAirport']) + '-' + str(list_flight[-1]['arrAirport']) + '-' + str(
      list_flight[0]['depTime'])[:8] + '-' + '@'.join([str(fly_i['flightNumber']) for fly_i in list_flight]),
    'flights': [{
      'segmentsList': [list_flight],
      'currency': 'CNY',
      'adultPrice': adultPrice,
      'adultTax': adultTax,
      'adultTotalPrice': adultTotalPrice,
    }],
    'status': 0,
    'msg': '',
    'siteCode': 'Qunargj',
    'datetime': int(str(list_flight[0]['depTime'])[:8]),
    'updatetime': int(time.time()),
  }
  return mongo_dict


def depair(start_data):
    cookie = get_cookie()
    if cookie.get('error') is None:
        data = get_data(start_data, cookie)
        try:
            if data.get('error') is None:
                exec_data(data['data'])
                flights_data['need'] = 0
                # print(flights_data)
            else:
                # print(data)
                flights_data['need'] = 1
                flights_data['result'] = []
                # print(flights_data)
        except Exception as e:
            print(f"{e}")
    else:
        # print(cookie)
        flights_data['need'] = 1
        flights_data['result'] = []
        print(flights_data)


if __name__ == '__main__':
    i = 1

    # 多线程版
    ip_dict = len(client8.keys())
    with concurrent.futures.ThreadPoolExecutor(2) as th:
        for items in range(ip_dict):
            pro_ip = proxy_ip()
            start_data = {
                'from': 'SHA',  # CDG
                'to': 'SEL',  # FOC
                'daytime': '2023-08-20',
                'adt_num': 1,
                'chd_num': '0',
                'inf_num': '0',
                'fly_num': '1',
                'limit_seat': '1',
                'proxy': pro_ip
            }
            th.submit(depair, start_data)
            i = i + 1


    # 单线程版
    # ip_dict = len(client8.keys())
    # for items in range(ip_dict):
    #     pro_ip = proxy_ip()
    #     start_data = {
    #         'from': 'SHA',  # CDG
    #         'to': 'SEL',  # FOC
    #         'daytime': '2023-08-20',
    #         'adt_num': 1,
    #         'chd_num': '0',
    #         'inf_num': '0',
    #         'fly_num': '1',
    #         'limit_seat': '1',
    #         'proxy': pro_ip
    #     }
    #     depair(start_data)
    #     i = i + 1