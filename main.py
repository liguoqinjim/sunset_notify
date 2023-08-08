import sys
import shutil
import pandas as pd
import json

from utils import send_msg_q_wechat

wx_token = sys.argv[1]
hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wx_token}"

new_filepath = "crawler/weibo/上海火烧云预测bot/7612166895.json"
old_filepath = "records/7612166895.json"

def get_new_content():
    with open(new_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # data['weibo']转为dataframe
    df_new = pd.DataFrame(data['weibo'])
    # df_new.drop(columns=['user_id','screen_name','source','comments_count','reposts_count','topics','at_users','created_at','article_url','video_url','attitudes_count','bid','location'],inplace=True)
    df_new = df_new[['id', 'full_created_at', 'text']]
    # 去除少于10个字符的内容
    df_new = df_new[df_new['text'].str.len() > 10]
    print(df_new)

    with open(old_filepath, "r", encoding="utf-8") as f:
        data_old = json.load(f)
    print(data_old)
    df_old = pd.DataFrame(data_old)
    print(df_old)
    # 获得df_old['full_created_at']的最大值
    max_full_created_at = df_old['full_created_at'].max()
    print(max_full_created_at)

    df = pd.concat([df_old, df_new], ignore_index=True)
    df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    df.sort_values(by='full_created_at', ascending=False, inplace=True)
    print(df)

    df_content = df.copy()
    df_content.sort_values(by='full_created_at', ascending=True, inplace=True)
    df_content = df_content.loc[df_content['full_created_at'] > max_full_created_at]
    df_content.reset_index(drop=True, inplace=True)
    print("content=")
    print(df_content)
    if len(df_content) > 0:
        texts = df_content['text'].tolist()
        content = ""
        for i, row in df_content.iterrows():
            content += f"第{i+1}条: {row['full_created_at']}" + "\n" + row['text'] + "\n"

        notify(content)

        with open(old_filepath, "w", encoding="utf-8") as f:
            f.write(df.to_json(orient='records', force_ascii=False, indent=4))
    else:
        print("无新内容")


    # 写入文件
    

def copy_record():
    shutil.copy(new_filepath, old_filepath)

def notify(content):
    send_msg_q_wechat(hook_url, content)

if __name__ == "__main__":
    get_new_content()
    exit()

    # 读取命令行参数


    # copy_record()
    notify(hook_url)