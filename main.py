import sys
import shutil
from utils import send_msg_q_wechat

def copy_record():
    # 复制文件到指定路径
    # filepath = "/Users/li/Workspace/github.com/sunset_notify/crawler/weibo/上海火烧云预测bot/7612166895.csv"
    filepath = "crawler/weibo/上海火烧云预测bot/7612166895.csv"
    new_dir = "records"

    shutil.copy(filepath, new_dir)

def notify(hook_url):
    send_msg_q_wechat(hook_url, "火烧云预测结果已更新")

if __name__ == "__main__":
    # 读取命令行参数
    wx_token = sys.argv[1]
    hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wx_token}"

    # copy_record()
    notify(hook_url)