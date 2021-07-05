import requests
import json
params = {
            "requestId": "id1",				
            "contentType":1,                 
            "data": {
                "contents": [
                    {
                        "content": "关键词1",  	# 关键词or 文本
                        "indust": 100010,   		# 关键词携带的客户资质行业
                        "acctId": 8696900      	# 账户id
                    },
                    {
                        "content": "关键词2",  	# 关键词or 文本
                        "indust": 100010,   		## 关键词携带的客户资质行业
                        "acctId": 8696900      	## 账户id
                    }
                ]
            }
}
url = "http://localhost:8000/indus-cls-api/indus-cls"
r = requests.post(url, params=params)
print(r)

url = "http://localhost:8000/hello"
r = requests.get(url)
print(r)
