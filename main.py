import sys
import shutil
import pandas as pd
import json

from utils import send_msg_q_wechat

new_filepath = "crawler/weibo/上海火烧云预测bot/7612166895.json"
old_filepath = "records/7612166895.json"

def get_new_content():
    with open(new_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data['weibo'])

    # data['weibo']转为dataframe
    df = pd.DataFrame(data['weibo'])
    df.drop(columns=['user_id','screen_name','source','comments_count','reposts_count','topics','at_users','created_at','article_url','video_url','attitudes_count','bid','location'],inplace=True)
    print(df)
    print(df.columns)
    df = df[['id', 'text', 'full_created_at']]

    # dataframe转为json数组
    df_json = df.to_json(orient='records', force_ascii=False, indent=4)

    # 写入文件
    with open(old_filepath, "w", encoding="utf-8") as f:
        f.write(df_json)

def copy_record():
    shutil.copy(new_filepath, old_filepath)

def notify(hook_url):
    send_msg_q_wechat(hook_url, "火烧云预测结果已更新")

if __name__ == "__main__":
    get_new_content()
    exit()

    # 读取命令行参数
    wx_token = sys.argv[1]
    hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wx_token}"

    # copy_record()
    notify(hook_url)