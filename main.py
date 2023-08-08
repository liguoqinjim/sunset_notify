import shutil

def copy_record():
    # 复制文件到指定路径
    filepath = "/Users/li/Workspace/github.com/sunset_notify/crawler/weibo/上海火烧云预测bot/7612166895.csv"
    new_dir = "records"

    shutil.copy(filepath, new_dir)


def notify():
    pass

if __name__ == "__main__":
    copy_record()