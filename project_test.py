import requests
import json
params = {"requestId": "id1",			
          "contentType":1,                 
          "data": {
                "contents": [
                    {
                        "content": "关键词1",  	
                        "indust": 100010,   		
                        "acctId": 8696900      	
                    },
                    {
                        "content": "关键词2",  	
                        "indust": 100010,   		
                        "acctId": 8696900      	
                    }
                ]
            }
}

headers = {'content-type': 'application/json'}

url = "http://172.17.0.4:8000/indus-cls-api/indus-cls"
r = requests.post(url, json=params, headers=headers)
print(r.text)

url = "http://172.17.0.4:8000/hello"
r = requests.get(url)
print(r)
