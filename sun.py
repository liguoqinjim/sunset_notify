import datetime
import json
import requests

def get_sun_time(key):
    """
    获得日出日落时间
    """
    # 获得今天和明天的日期，格式为"20230825"
    today = datetime.date.today().strftime('%Y%m%d')
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')

    content = ""
    location_id = 101020100 # 上海
    for n,date in enumerate([today, tomorrow]):
        url = f"https://devapi.qweather.com/v7/astronomy/sun?location={location_id}&date={date}&key={key}"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)

        sunrise_time = datetime.datetime.strptime(data['sunrise'], '%Y-%m-%dT%H:%M%z').time()
        sunset_time = datetime.datetime.strptime(data['sunset'], '%Y-%m-%dT%H:%M%z').time()

        content += f"{'今日' if n == 0 else '明日'}日出时间: {sunrise_time}，日落时间: {sunset_time}\n"

    return content
