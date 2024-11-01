from datetime import datetime
import json
import traceback
import requests
import os
import base64
import hashlib
import urllib
import time
from PIL import Image


def request_with_retry(target_url, headers, payload, timeout=10, max_retries=3, retry_interval=5):
    """
    发送带有超时和重试的 HTTP 请求
    :param target_url: 请求的 URL
    :param headers: 请求头
    :param payload: 请求体
    :param timeout: 超时时间，单位为秒
    :param max_retries: 最大重试次数
    :param retry_interval: 重试间隔时间，单位为秒
    :return: HTTP 响应
    """
    for i in range(max_retries):
        try:
            response = requests.request("GET", target_url, headers=headers, data=payload, timeout=timeout)
            return response
        except requests.exceptions.Timeout:
            print(f"请求超时，正在进行第 {i + 1} 次重试...")
            time.sleep(retry_interval)
    raise requests.exceptions.Timeout(f"请求超时，已重试 {max_retries} 次")


def send_msg_q_wechat(hook_url, content):
    try:
        data = {"msgtype": "text", "text": {"content": content}}
        r = requests.post(hook_url, data=json.dumps(data), timeout=5)
        print(f"调用企业微信接口返回： {r.text}")
        print("成功发送企业微信")
    except Exception as e:
        print(f"发送企业微信失败:{e}")
        print(traceback.format_exc())


class MyEncoder(json.JSONEncoder):
    """
    定义一个JSON编码器，用来处理默认json无法转换的数据类型，例如：图片
    """

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# 企业微信发送图片
def send_wechat_work_img(wechat_webhook_url, file_path):
    """
    企业微信发送图片
    :param file_path:       本地图片的位置
    :return:
    """
    try:
        # 判断图片是否存在
        if not os.path.exists(file_path):  # 图片不存在，跳过该程序
            print('找不到图片')
            return
        # 读取图片文件
        with open(file_path, 'rb') as f:
            image_content = f.read()
        image_base64 = base64.b64encode(image_content).decode('utf-8')  # 将图片进行编码，转成base64格式
        md5 = hashlib.md5()  # 构建md5
        md5.update(image_content)  # 对于base64格式的图片进行md5加密
        image_md5 = md5.hexdigest()  # 获取图片加密后的hex码，这就是常见的md5码
        data = {
            'msgtype': 'image',
            'image': {
                'base64': image_base64,
                'md5': image_md5
            }
        }
        # 服务器上传bytes图片的时候，json.dumps解析会出错，需要自己手动去转一下
        r = requests.post(wechat_webhook_url, data=json.dumps(data, cls=MyEncoder, indent=4), timeout=10, proxies=None)
        print(f'调用企业微信接口返回： {r.text}')
        print('成功发送企业微信')
    except Exception as e:
        print(f"发送企业微信失败:{e}")
        print(traceback.format_exc())
    finally:
        # 判断图片是否存在
        if os.path.exists(file_path):  # 不管有没有发送成功，最后都去删除图片
            os.remove(file_path)


# 百度OCR识别图片
def _baidu_get_access_token(api_key, secret_key):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def baidu_ocr(image_filepath, api_key, secret_key):
    url = (
            "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token="
            + _baidu_get_access_token(api_key, secret_key)
    )

    payload = get_file_content_as_base64(image_filepath, True)

    # image 可以通过 get_file_content_as_base64("C:\fakepath\Snipaste_2023-09-12_22-15-53.jpg",True) 方法获取
    payload = f"image={payload}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    # 保存结果到文件
    return _baidu_ocr_content_wrap(response.json())


def _baidu_ocr_content_wrap(ocr_result):
    """
    整理百度OCR识别结果
    """

    full_text = ""
    for i, word_info in enumerate(ocr_result["words_result"]):
        text = word_info["words"]
        if i > 0:
            # 如果不是第一个文本块，检查是否需要换行
            prev_top = ocr_result["words_result"][i - 1]["location"]["top"]
            current_top = word_info["location"]["top"]
            if current_top - prev_top > 10:
                full_text += "\n"
        full_text += text

    return full_text


def get_pic_url():
    target_url = (
        "https://sunsetbot.top/"
    )

    payload = {}
    headers = {
        # "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    # response = requests.request("GET", target_url, headers=headers, data=payload)
    response = request_with_retry(target_url, headers, payload, timeout=20, max_retries=3, retry_interval=5)

    # 从response的HTML中，找出图片的URL
    soup = BeautifulSoup(response.text, 'html.parser')
    img_rise = soup.select_one('#rise_img_src')['src']
    img_rise = "https://sunsetbot.top" + img_rise

    img_set = soup.select_one('#set_img_src')['src']
    img_set = "https://sunsetbot.top" + img_set
    print(img_rise, img_set)
    return img_rise, img_set


def download_sunset_image(image_url, rise=True, save_dir="temp"):
    """
    下载图片
    """
    # target_url = (
    #     "https://sunsetbot.top/static/media/cross_section/%E4%B8%8A%E6%B5%B7_rise.png"
    # )
    filename = "rise.png"
    if not rise:
        target_url = "https://sunsetbot.top/static/media/cross_section/%E4%B8%8A%E6%B5%B7_set.png"
        filename = "set.png"

    payload = {}
    headers = {
        # "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    # response = requests.request("GET", target_url, headers=headers, data=payload)
    response = request_with_retry(image_url, headers, payload, timeout=20, max_retries=3, retry_interval=5)

    # 保存为图片
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    _filepath = os.path.join(save_dir, filename)

    with open(_filepath, "wb") as f:
        f.write(response.content)

    return _filepath


def split_image(image_filepath):
    """
    切割图片
    """
    # 读取图片
    from PIL import Image

    im = Image.open(image_filepath)
    # 获取图片的宽度和高度
    img_size = im.size
    print("img_size:", img_size)

    # (1385,400-78)  到(1626,652-78)
    xy1 = (1385, 400 - 78)
    xy2 = (1626, 652 - 78)
    # 切割图片
    region = im.crop(xy1 + xy2)

    # 保存图片，在文件名后面加一个split，需要加载后缀名的前面
    _filepath = image_filepath.split(".")
    _filepath = _filepath[0] + "_split." + _filepath[1]
    region.save(_filepath)

    return _filepath


def compress_png_to_webp(input_path, output_path, quality, lossless=False):
    """
    将 PNG 图片压缩为 WebP 格式
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    :param quality: 压缩质量，介于 1 到 100 之间
    :param lossless: 是否使用无损压缩
    """
    with Image.open(input_path) as im:
        im.save(output_path, format="webp", quality=quality, lossless=lossless)
