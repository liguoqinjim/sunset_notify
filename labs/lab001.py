import requests

def download_png():
    """
    下载图片
    """

    url = "https://sunsetbot.top/static/media/cross_section/%E4%B8%8A%E6%B5%B7_rise.png"

    payload = {}
    headers = {
        'Host': 'sunsetbot.top',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # 保存为图片
    with open("test.png", "wb") as f:
        f.write(response.content)

def split_image():
    """
    切割图片
    """
    # 读取图片
    from PIL import Image
    im = Image.open("test.png")
    # 获取图片的宽度和高度
    img_size = im.size
    print(img_size)

    # (1385,400-78)  到(1626,652-78)
    xy1 = (1385,400-78)
    xy2 = (1626,652-78)
    # 切割图片
    region = im.crop(xy1 + xy2)
    # 保存图片
    region.save("test2.png")
    
def baidu_ocr():
    """
    百度OCR识别图片
    """

if __name__ == '__main__':
    # download_png()
    # split_image()
    baidu_ocr()