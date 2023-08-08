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

    # data['weibo']转为dataframe
    df_new = pd.DataFrame(data['weibo'])
    df_new.drop(columns=['user_id','screen_name','source','comments_count','reposts_count','topics','at_users','created_at','article_url','video_url','attitudes_count','bid','location'],inplace=True)
    df_new = df_new[['id', 'full_created_at', 'text']]
    # df_new['full_created_at'] = pd.to_datetime(df_new['full_created_at'])

    # with open(old_filepath, "r", encoding="utf-8") as f:
    #     data_old = json.load(f)
    # print(data_old)
    # df_old = pd.DataFrame(data_old)
    # print(df_old)

    # 写入文件
    with open(old_filepath, "w", encoding="utf-8") as f:
        # dataframe转为json数组
        df_json = df_new.to_json(orient='records', force_ascii=False, indent=4)
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