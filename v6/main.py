from functions import *
import time
from datetime import datetime
import sys
import requests

# 读取参数
wx_token = sys.argv[1]
hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wx_token}"


def notify(content):
    send_msg_q_wechat(hook_url, content)


def process_image(img_path):
    print("处理:", img_path)

    # 对图片进行切割
    img_split_path = split_image(img_path)
    print("split_image:", img_split_path)

    # 对图片进行压缩
    save_dir = "records/images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    phase = "rise" if "rise" in img_path else "set"
    new_img_path = os.path.join(
        save_dir, f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}_{phase}.webp"
    )

    compress_png_to_webp(img_path, new_img_path, quality=10)

    # 返回
    return img_split_path


def process_report(report_rise, report_set):
    """
    处理火烧云报告
    """

    # 通知微信
    # notify(content)
    today = datetime.now().strftime("%Y-%m-%d")
    send_msg_q_wechat(hook_url, f"{today}火烧云报告:日出")
    time.sleep(1)
    send_wechat_work_img(hook_url, report_rise)
    time.sleep(1)

    send_msg_q_wechat(hook_url, f"{today}火烧云报告:日落")
    time.sleep(1)

    send_wechat_work_img(hook_url, report_set)


def get_info_from_api(event="rise_1"):
    events_dict = {
        "rise_1": "今日日出",
        "rise_2": "明日日出",
        "set_1": "今日日落",
        "set_2": "明日日落",
    }
    if event not in events_dict:
        raise ValueError("event参数错误")

    # 获取API返回
    # url = "https://sunsetbot.top/?query_city=&event_date=None&event=rise_2&times=None&intend=select_city"
    url = f"https://sunsetbot.top/?query_city=&event_date=None&event={event}&times=None&intend=select_city"

    payload = {}

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
        "Connection": "keep-alive",
        "Cookie": 'city_name="\\344\\270\\212\\346\\265\\267"; city_name="\\344\\270\\212\\346\\265\\267"',
        "Referer": "https://sunsetbot.top/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    event_time = data['tb_event_time'].replace("<br>", " ")
    quality = data['tb_quality'].replace("<br>", " ")
    aod = data['tb_aod'].replace("<br>", " ")

    # 发送微信通知
    title = f"{events_dict[event]}:\n"
    msg = f"北京时间：{event_time}\n火烧云鲜艳度：{quality}\n大气透明度：{aod}"

    content = f"{title}\n{msg}"
    send_msg_q_wechat(hook_url, content)


def is_before_sunrise():
    """
    判断现在是否为日出之前，也就是凌晨
    """
    now = datetime.now()
    sunrise_time = datetime(now.year, now.month, now.day, 5, 0, 0)  # 设置日出时间为早上5点
    return now.hour < sunrise_time.hour


def is_after_sunset():
    """
    判断现在是否为日落之后，也就是晚上
    """
    now = datetime.now()
    sunset_time = datetime(now.year, now.month, now.day, 20, 0, 0)  # 设置日落时间为晚上7点
    return now.hour > sunset_time.hour


def get_info():
    before_sunrise = is_before_sunrise()
    after_sunset = is_after_sunset()

    if before_sunrise:  # 今日日出和今日日落
        get_info_from_api(event="rise_1")
        time.sleep(2)
        get_info_from_api(event="set_1")
    else:
        if not after_sunset:  # 今日日落和明日日出
            get_info_from_api(event="set_1")
            time.sleep(2)
            get_info_from_api(event="rise_2")
        else:  # 日落之后，明日日出和明日日落
            get_info_from_api(event="rise_2")
            time.sleep(2)
            get_info_from_api(event="set_2")


def run():
    """
    获得火烧云数据
    """
    get_info()


if __name__ == "__main__":
    run()
