from datetime import datetime
import json
import traceback
import requests

def send_msg_q_wechat(hook_url,content):
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        r = requests.post(hook_url, data=json.dumps(data), timeout=10)
        print(f'调用企业微信接口返回： {r.text}')
        print('成功发送企业微信')
    except Exception as e:
        print(f"发送企业微信失败:{e}")
        print(traceback.format_exc())


# 企业微信发送图片
def send_images_q_wechat(base64_data, md5_data):
    try:
        data = {
            "msgtype": "image",
            "image": {
                "base64": base64_data,
                "md5": md5_data
            }
        }
        # 又是一个小细节，服务器上传bytes图片的时候，json.dumps解析会出错，需要自己手动去转一下
        r = requests.post(wechat_webhook_url, data=json.dumps(data, cls=MyEncoder, indent=4), timeout=10)
        print(f'调用企业微信接口返回： {r.text}')
        print('成功发送企业微信')
    except Exception as e:
        print(f"发送企业微信失败:{e}")
        print(traceback.format_exc())
