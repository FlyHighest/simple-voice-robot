from .enums import LISTEN_STATUS
from .wav_utils import (concat_multi_wav_files,
                        get_wav_volume)
                       
import time 

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))