from .robot import Robot
from utils import (extract_location, extract_time, 
                   get_location_id,get_24h_weather,
                   get_now_weather,get_3d_weather,
                   diff_now_hours,get_hours_between)
from datetime import datetime

class WeatherBot(Robot):

    def __init__(self) -> None:
        super().__init__()

    def special_weather_care(self,text,response):
        if "雨" in response or "雪" in response:
            response += "记得带伞。"
        if "雾" in response or "霾" in response or "沙" in response or "尘" in response:
            response += "天气不好，外出请注意安全。"
        return response

    def reply(self, text):
        location = extract_location(text)
        location_id,location_name = get_location_id(location)
        query_time = extract_time(text)
        # 时间：
        # 没有给定时间：默认当前、默认地点的天气，调用get_now_weather
        # 给定时间点、时间段，且在24小时内：调用get_24h_weather
        # 给定时间，但在24小时之外：调用get_3d_weather
        if query_time == "now":
            res = get_now_weather(location_id=location_id)
            temp = res['temp']
            wind = res['wind']
            text = res['text']
            response = f"{location_name}当前天气:{text}，温度{temp}度，风力等级{wind}级。"
            response = self.special_weather_care(text, response)
        else:
            query_time_start, query_time_end = query_time 
            diff_now = diff_now_hours(query_time_end)
            if diff_now < 0:
                response = '抱歉，我仅能获取未来天气。'
            elif diff_now<24:
                # 构造未来的小时整点时间列表
                time_points, start_hour, end_hour = get_hours_between(query_time_start,query_time_end)
                start_time = datetime.fromisoformat(query_time_start)
                month = start_time.month
                day = start_time.day

                res = get_24h_weather(location_id,time_points)

                response = f"{location_name}{month}月{day}日"
                if start_hour==end_hour:
                    response += f"{start_hour}点"
                else:
                    response += f"{start_hour}点到{end_hour}点"
                response += f"天气: {res['text']}，"
                response += f"温度{res['temp'][0]}到{res['temp'][1]}度。"
                response += f"风力最大{res['wind']}级。"
                response = self.special_weather_care(text,response)
            else:
                res = get_3d_weather(location_id,query_time_end)
                end_time = datetime.fromisoformat(query_time_end)
                month = end_time.month
                day = end_time.day
                response = f"{location_name}{month}月{day}日"
                if res['text'][0] == res['text'][1]:
                    response += f"天气：{res['text'][0]}。"
                else:
                    response += f"白天：{res['text'][0]}，夜间：{res['text'][1]}。"
                response += f"温度{res['temp'][0]}到{res['temp'][1]}度。"
                if res['wind'][0] == res['wind'][1]:
                    response += f"风力{res['wind'][0]}级。"
                else:
                    response += f"白天风力{res['wind'][0]}级，夜间风力{res['wind'][1]}级"
                response = self.special_weather_care(text,response)

        return response
