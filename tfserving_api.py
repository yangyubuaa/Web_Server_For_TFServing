from transformers import BertTokenizer
import requests
import json

# 每个字符串分别调用一次接口
def tfserving_request_lazy(tokenizer, keywordList):
    ret_list = list()
    for user_input in keywordList:
        tokenized = tokenizer(user_input, max_length=64, truncation=True, padding="max_length")
        print(tokenized)
        input_ids = [tokenized["input_ids"]]
        token_type_ids = [tokenized["token_type_ids"]]
        attention_mask = [tokenized["attention_mask"]]

        # docker.for.mac.host.internal
        url = "http://10.160.35.116:8501/v1/models/albert_cls_pb/versions/2:predict"
        # url = "http://localhost:8501/v1/models/albert_cls_pb/versions/1:predict"
        headers = {'content-type': 'application/json'}

        data = {
            "inputs":{
                "token_type_ids": token_type_ids,
                "attention_mask": attention_mask,
                "input_ids": input_ids
            }
        }

        r = requests.post(url, json=data, headers=headers)
        print(r.status_code)
        logits = json.loads(r.text)['outputs']['loss']
        print(logits[0])
        ret_list.append(logits[0])
    return ret_list

# 将字符串组成batch只调用一次接口
def tfserving_request(tokenizer, keywordList):
    tokenized = tokenizer(keywordList, max_length=64, truncation=True, padding="max_length")

    input_ids = tokenized["input_ids"]
    token_type_ids = tokenized["token_type_ids"]
    attention_mask = tokenized["attention_mask"]

    print(input_ids)

    # docker.for.mac.host.internal
    url = "http://10.160.35.116:8501/v1/models/albert_cls_pb_batch/versions/1:predict"
    # url = "http://localhost:8501/v1/models/albert_cls_pb/versions/1:predict"
    headers = {'content-type': 'application/json'}

    data = {
        "inputs":{
            "token_type_ids": token_type_ids,
            "attention_mask": attention_mask,
            "input_ids": input_ids
        }
    }

    r = requests.post(url, json=data, headers=headers)
    print(r.text)

if __name__ == "__main__":
    tokenizer = BertTokenizer.from_pretrained("model_transfer/albert_tiny_pytorch")
    keywordList = [
        "今天天气怎么样",
        "网络游戏好玩吗",
        "英雄联盟怎么才能赢"
    ]
    tfserving_request_lazy(tokenizer, keywordList)
    # tfserving_request(tokenizer, keywordList)