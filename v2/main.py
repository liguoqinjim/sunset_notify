from functions import *
from llm import *
import time
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

    # 调用百度OCR识别图片
    ocr_content = baidu_ocr(img_split_path, baidu_ocr_api_key, baidu_ocr_secret_key)
    print("ocr_content:---------------\n", ocr_content)
    print("ocr_content:---------------")

    # 调用llm
    report = get_llm_quality_report(ocr_content)
    print("report:", report)

    # report转为dict
    report_dict = report.dict()
    report_dict["origin"] = ocr_content
    print(report_dict)

    if "rise" in img_path:
        assert report_dict["phase"] == "日出"
    else:
        assert report_dict["phase"] == "日落"

    # 对图片进行压缩
    save_dir = "records/images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    new_img_path = os.path.join(
        save_dir, f"{report_dict['date']}_{report_dict['phase']}.webp"
    )

    compress_png_to_webp(img_path, new_img_path, quality=10)
    report_dict["image_path"] = new_img_path

    # 返回
    return report_dict


def process_report(report_rise, report_set):
    """
    处理火烧云报告
    """

    # 整理内容
    reports = [report_rise, report_set]
    # 把reports保存为json
    save_dir = "records/json"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 保存json, 以系统日期命名，格式"20230913_2239.json"
    json_path = os.path.join(save_dir, f"{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(json_path, "w") as f:
        json.dump(reports, f, ensure_ascii=False, indent=4)

    # 对reports排序，按照日期、时间排序
    reports = sorted(reports, key=lambda x: (x["date"], x["time"]))

    content = ""
    for _r in reports:
        _c = f"{_r['date']} {_r['time']} {_r['phase']} {_r['quality']} {_r['quality_report']}\n"
        content += _c

    # 通知微信
    notify(content)


def run():
    """
    获得火烧云数据
    """
    # 下载日落日出图片
    img_rise = download_sunset_image(rise=True,save_dir="temp")
    time.sleep(3)
    img_set = download_sunset_image(rise=False,save_dir="temp")

    print("img_rise:",img_rise)
    print("img_set:",img_set)

    # 处理图片
    report_rise = process_image(img_rise)
    report_set = process_image(img_set)

    # 处理结果
    process_report(report_rise, report_set)


if __name__ == "__main__":
    run()
    # process_image("temp/rise.png")
