from functions import *
import time
from datetime import datetime
import sys
import requests
from bs4 import BeautifulSoup

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


def get_info_from_api(rise=True):
    # 获取API返回
    if rise:
        url = "https://sunsetbot.top/?query_city=&times=None&event=rise"
    else:
        url = "https://sunsetbot.top/?query_city=&times=None&event=set"
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

    html_content = data["table_content"]
    soup = BeautifulSoup(html_content, "html.parser")

    # 找到所有的 <tr> 标签
    tr_tags = soup.find_all("tr")

    # 如果找到了至少两个 <tr> 标签
    if len(tr_tags) == 2:
        # 获取元数据内容
        first_tr = tr_tags[0]
        first_tds = first_tr.find_all("td")
        first_p_contents = [td.find("p").text.strip() for td in first_tds if td.find("p")]
        print(first_p_contents)

        # 获取第二个 <tr> 标签
        second_tr = tr_tags[1]
        # 找到所有的 <td> 标签
        td_tags = second_tr.find_all("td")
        # 对每个 <td> 标签，找到其子元素 <p> 的内容
        p_contents = [td.find("p").text.strip() for td in td_tags if td.find("p")]
        print(p_contents)

        # 发送微信通知
        title = "日出:" if rise else "日落:"
        msg = ""

        for i,content in enumerate(first_p_contents):
            if i == len(p_contents) - 1:
                continue

            msg += f"{content}:{p_contents[i]}\n"

        content = f"{title}\n{msg}"
        send_msg_q_wechat(hook_url, content)
    else:
        print("没有找到至少两个 <tr> 标签")

def run():
    """
    获得火烧云数据
    """
    get_info_from_api(rise=True)
    time.sleep(2)
    get_info_from_api(rise=False)


if __name__ == "__main__":
    run()
