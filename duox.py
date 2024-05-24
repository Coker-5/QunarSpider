
import redis


client = redis.Redis(host="localhost",port=6379,decode_responses=True,db=5)
ip_dict = client.keys()
ip_dict = client.mget(ip_dict)
for items in ip_dict:
	print(items)