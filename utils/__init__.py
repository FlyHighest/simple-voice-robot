from .enums import LISTEN_STATUS
from .wav_utils import (concat_multi_wav_files,
                        get_wav_volume,
                        convert_mp3_to_wav)
from .info_extract import extract_location,extract_time
from .weather import get_location_id, get_24h_weather, get_now_weather,get_3d_weather
import time,pytz

from datetime import datetime, timedelta

def get_hours_between(start_time_str, end_time_str):
    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.fromisoformat(end_time_str)
    hour_list = []
    if start_time.minute==0 and start_time.second==0:
        hour_list.append(start_time.astimezone(pytz.timezone('Asia/Shanghai')).isoformat('T',timespec="minutes"))
        start_hour = start_time.hour 
    else:
        start_hour = start_time.hour + 1
    end_hour = start_hour
    for hour in range(start_time.hour, end_time.hour):
        hour_time = start_time.replace(hour=hour, minute=0, second=0) + timedelta(hours=1)
        hour_list.append(hour_time.astimezone(pytz.timezone('Asia/Shanghai')).isoformat('T',timespec="minutes"))
        end_hour = hour_time.hour

    return hour_list, start_hour, end_hour

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def current_isotime():
    now = datetime.now()
    iso_now = now.astimezone(pytz.timezone('Asia/Shanghai')).isoformat('T',timespec="minutes")
    return iso_now


def diff_hours(time_str1, time_str2):
    time1 = datetime.fromisoformat(time_str1)
    time2 = datetime.fromisoformat(time_str2)
    diff = time2 - time1
    diff_hours = diff.total_seconds() / 3600
    return diff_hours


def diff_now_hours(time_str):
    return diff_hours(current_isotime(), time_str)