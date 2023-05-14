import httpx 
import json 
from config import cfg 
from functools import lru_cache
# 获取方式：
# 地点：没有给定则默认地点，给定则使用给定地点


api_key = cfg.api.qweather_key

@lru_cache(maxsize=32)
def get_location_id(location=None):
    global api_key
    if location is None:
        url = f"https://geoapi.qweather.com/v2/city/lookup?key={api_key}&location={cfg.settings.location}"
    else:
        url = f"https://geoapi.qweather.com/v2/city/lookup?key={api_key}&location={location}"
    res = httpx.get(url)
    if res.status_code==200 :
        res_json = json.loads(res.content.decode())
        if res_json['code']!='200':
            return "101010100","北京"
        loc = res_json['location'][0]
        return  loc['id'],loc['name']
    else:
        if location is not None:
            return get_location_id()
        else:
            return "101010100","北京"

def filter_weather(L):
    normal_weather = ["阴", "晴", "多云","少云","晴间多云"]
    for weather in L:
        if weather not in normal_weather:
            return [w for w in L if w not in normal_weather]
    return L

def get_now_weather(location_id):
    global api_key
    url = f"https://devapi.qweather.com/v7/weather/now?key={api_key}&location={location_id}"
    res = httpx.get(url)
    if res.status_code==200:
        res_json = json.loads(res.content.decode())
        if res_json['code']!='200':
            return None 
        
        return {
            "temp": res_json['now']["temp"],
            "text": res_json['now']['text'],
            "wind": res_json['now']['windScale'].replace("-","到")
        }
    else:
        return None


def get_24h_weather(location_id, time_points:list):
    # 时间列表要给iso 8601标准的时间字符串
    global api_key
    url = f"https://devapi.qweather.com/v7/weather/24h?key={api_key}&location={location_id}"
    res = httpx.get(url)
    if res.status_code==200:
        res_json = json.loads(res.content.decode())
        if res_json['code']!='200':
            return None 
        
        temps = []
        texts = set()
        winds = []
        print(res_json['hourly'])
        print(time_points)
        for weather_info in res_json['hourly']:
            if weather_info['fxTime'] in time_points:
                temps.append(int(weather_info['temp']))
                texts.add(weather_info['text'])
                winds.append(weather_info['windScale'])
        
        if len(texts)==0:
            return None 
        # 如有特殊天气，则删除texts中的普通天气
        texts = filter_weather(texts)
        res_temp = [str(min(temps)),str(max(temps))]
        winds.sort()
        res_wind = winds[-1] # 最大风速
        
        return {
            "temp": res_temp,
            "text": ",".join(texts),
            "wind": res_wind.replace("-","到")
        }
    else:
        return None

def get_3d_weather(location_id, time_point):
    # 时间要给iso 8601标准的时间字符串
    global api_key
    url = f"https://devapi.qweather.com/v7/weather/3d?key={api_key}&location={location_id}"
    res = httpx.get(url)
    if res.status_code==200:
        res_json = json.loads(res.content.decode())
        if res_json['code']!='200':
            return None 

        res_temp = []
        for weather_info in res_json['daily']:
            if weather_info['fxDate'] == time_point.split("T")[0]:
                res_temp = [weather_info['tempMin'],weather_info['tempMax']]
                res_text = [weather_info['textDay'],weather_info['textNight']]
                res_wind = [weather_info['windScaleDay'].replace("-","到"),weather_info['windScaleNight'].replace("-","到")]
        if len(res_temp)==0:
            return None 
        return {
            "temp": res_temp,
            "text": res_text,
            "wind": res_wind
        }
    else:
        return None
