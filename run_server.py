import time
import json
import numpy as np
from flask import Flask
from flask import request
app = Flask(__name__)

from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained("model_transfer/albert_tiny_pytorch")

from tfserving_api import tfserving_request_lazy, tfserving_request

@app.route('/hello')
def predict():
    return "helloworld!"


@app.route("/indus-cls-api/indus-cls", methods=["POST", "GET"])
def indus_cls_refuse():
    try:
        # 参数解析
        params = request.get_data()
        params = json.loads(params)
        print(params)
        
    
        keywords = params["data"]["contents"]
        keywordList = []
        for kwd in keywords:
            keywordList.append(kwd["content"])

        print(keywordList)
        start_predict = time.time()
        # 调用TFServing进行模型预测
        
        # tfserving_request(tokenizer, keywordList)
        ret_list = tfserving_request_lazy(tokenizer, keywordList)

        end_predict = time.time()
        print('predict use time:', end_predict - start_predict)
        print(ret_list)
        print(len(ret_list))

        # 结果返回
        ret = {"result": 200}
        ret['requestId'] = params["requestId"]
        ret['contentType'] = params["contentType"]

        ret['data'] = params["data"]
        print("____")
        # ret['data']['rst'] = ret_list
        for idx, val in enumerate(ret_list, 0):
            pred = np.argmax(val)
            # print('pred: ',pred)
            if ret['data']["contents"][idx]["indust"] == 2040202:
                if  pred==0 or pred==8 or pred==1 or len(ret['data']["contents"][idx]["content"] )<=3:
                    # if val[pred] > 0.95:
                    #     ret['data']["contents"][idx]["category_code"] = 10007 #自动通过
                    # else:
                    ret['data']["contents"][idx]["category_code"] = 10000 #自动通过
                else:
                    ret['data']["contents"][idx]["category_code"] = 10009 #行业不相关
            elif ret['data']["contents"][idx]["indust"] == 2040201:
                if  pred==8 or len(ret['data']["contents"][idx]["content"] )<=3 :
                    ret['data']["contents"][idx]["category_code"] = 10000
                else:
                    ret['data']["contents"][idx]["category_code"] = 10009 #棋牌开发拒绝
            elif ret['data']["contents"][idx]["indust"] == 2040203:
                if  pred==0 or len(ret['data']["contents"][idx]["content"] )<=3:
                    # if val[pred] > 0.95:
                    #     ret['data']["contents"][idx]["category_code"] = 10007 #自动通过
                    # else:
                    ret['data']["contents"][idx]["category_code"] = 10000 #自动通过
                else:
                    ret['data']["contents"][idx]["category_code"] = 10009 #行业不相关
            elif ret['data']["contents"][idx]["indust"] == 2041500 :
                if pred == 1 or len(ret['data']["contents"][idx]["content"] )<=3:
                    ret['data']["contents"][idx]["category_code"] = 10000
                else:
                    ret['data']["contents"][idx]["category_code"] = 10009
            # elif ret['data']["contents"][idx]["indust"] == 2070100 :
            #     if pred == 2 or len(ret['data']["contents"][idx]["content"] )<=3:
            #         ret['data']["contents"][idx]["category_code"] = 10000
            #     else:
            #         ret['data']["contents"][idx]["category_code"] = 10009
            # elif ret['data']["contents"][idx]["indust"] == 2110300 :
            #     if pred == 4 or len(ret['data']["contents"][idx]["content"] )<=3:
            #         ret['data']["contents"][idx]["category_code"] = 10000
            #     else:
            #         ret['data']["contents"][idx]["category_code"] = 10009
            # elif ret['data']["contents"][idx]["indust"] == 2081800 : # 保健食品
            #     if pred == 5 or pred == 8 or len(ret['data']["contents"][idx]["content"] )<=3:
            #         ret['data']["contents"][idx]["category_code"] = 10000
            #     else:
            #         ret['data']["contents"][idx]["category_code"] = 10009
            # elif ret['data']["contents"][idx]["indust"] == 2080800:
            #         if pred==6 or pred == 8 or len(ret['data']["contents"][idx]["content"] )<=3:
            #             ret['data']["contents"][idx]["category_code"] = 10000
            #         else:
            #             ret['data']["contents"][idx]["category_code"] = 10009
            else:
                ret['data']["contents"][idx]["category_code"] = 10000

            ret['data']["contents"][idx]["probability"] = str(pred) + '|' + str(val[pred])
            # ret['data']["keywords"][idx]["probability"] = round(y_score[idx],2)
        ret = json.dumps(ret, ensure_ascii=False)
        return ret
        
    except Exception as e:
        print('print error:', str(e))
        ret = {"result": 500}
        ret = json.dumps(ret, ensure_ascii=False)
        return ret
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)