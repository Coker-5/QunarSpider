import random
import threading
import time

import redis

# client = redis.Redis(host="10.0.1.130", port=63790,decode_responses=True, db=5, password="yun_4827")
# ip_dict = client.keys()
# ip_dict = client.mget(ip_dict)
# print(len(ip_dict))

# def proxy_ip():
#     while True:
#         time.sleep(random.uniform(0.02, 0.04))
#         try:
#             key_name = client.randomkey()
#             cd_data_redis = client.get(key_name)
#             cd_data = str(cd_data_redis.decode())
#             print(cd_data)
#             break
#         except Exception as e:
#             print(e)
#             print(1)
#             print('jiuyuan IP redis:%s' % str(e), flush=True)
#     return str(cd_data)


ip_pool = redis.ConnectionPool(host='124.232.153.85', port=63799, db=int(0), max_connections=1000)
client = redis.Redis(connection_pool=ip_pool, password="yun_4827")
print(client.dbsize())
c = client.randomkey()
b = client.hmget("dd", "cookie")
print(b)
if b == [None]:
    print(123)
else:
    print(555)
# for item in range(ip_dict):
#     threds = threading.Thread(target=proxy_ip)
#     threds.start()


#
#
# if __name__ == '__main__':
#     print(proxy_ip())

