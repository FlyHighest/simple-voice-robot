from typing import Any
from .robot import Robot
import socket 
import time 

# 获取本地IP地址
def get_local_ip():
    # 创建一个socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 连接外部不存在的IP地址，不会真正发送数据
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()

    return ip

class SysInfoBot(Robot):
    def __init__(self) -> None:
        super().__init__()
    
    def reply(self, text):
        response = ""
        if "IP" in text:
            response += f"IP地址是{get_local_ip()}。"
        if "时间" in text:
            localtime = time.localtime()
            response += f"系统时间是{localtime.tm_hour}点{localtime.tm_min}分。"
        if "CPU温度" in text:
            response += f"CPU温度为{int(open('/sys/class/thermal/thermal_zone0/temp').read().strip())//1000}度"
        return response
        