import requests
import json


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"
}
cookies = {
    "QN1": "20230810",
    "QN48": "20230810"
}
url = "https://pwapp.qunar.com/api/log/commonLog"
params = {
    "pt": "www"
}
data = {
    "action": [
        {
            "operType": "show",
            "pageUrl": "https://flight.qunar.com/site/oneway_list_inter.htm",
            "operTime": 1691397622205
        }
    ]
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

print(response.text)
print(response)