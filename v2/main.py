from functions import *
import time
import sys

# 读取参数
baidu_ocr_api_key = sys.argv[1]
baidu_ocr_secret_key = sys.argv[2]

def process_image(img_path):
    print("处理:",img_path)

    # 对图片进行切割
    img_split_path = split_image(img_path)

    # 调用百度OCR识别图片
    ocr_content = baidu_ocr(img_split_path, baidu_ocr_api_key, baidu_ocr_secret_key)
    print("ocr_content:",ocr_content)

def run():
    """
    获得火烧云数据
    """
    # 下载日落日出图片
    img_rise = download_sunset_image(rise=True,save_dir="temp")
    time.sleep(3)
    img_set = download_sunset_image(rise=False,save_dir="temp")

    print(img_rise)
    print(img_set)

    # 处理图片


if __name__ == '__main__':
    # run()
    process_image("temp/rise.png")