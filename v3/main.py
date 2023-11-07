from functions import *
import time
from datetime import datetime
import sys

# 读取参数
baidu_ocr_api_key = sys.argv[1]
baidu_ocr_secret_key = sys.argv[2]
wx_token = sys.argv[3]
# weather_api_key = sys.argv[2]
hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wx_token}"


def notify(content):
    send_msg_q_wechat(hook_url, content)


def process_image(img_path):
    print("处理:", img_path)

    # 对图片进行切割
    img_split_path = split_image(img_path)
    print("split_image:",img_split_path)

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

def run():
    """
    获得火烧云数据
    """
    # 获得图片url
    img_rise_url ,img_set_url = get_pic_url()

    # 下载日落日出图片
    img_rise = download_sunset_image(img_rise_url,rise=True,save_dir="temp")
    time.sleep(1)
    img_set = download_sunset_image(img_set_url,rise=False,save_dir="temp")

    print("img_rise:",img_rise)
    print("img_set:",img_set)

    # 处理图片
    report_rise_image_path = process_image(img_rise)
    report_set_image_path = process_image(img_set)

    # 处理结果
    process_report(report_rise_image_path, report_set_image_path)


if __name__ == "__main__":
    run()
    # process_image("temp/rise.png")
