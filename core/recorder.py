from utils import LISTEN_STATUS
import subprocess
import wave 
import os 
import time 
import numpy as np 
from multiprocessing import Process,Value 
from utils import get_wav_volume,concat_multi_wav_files
from collections import deque
import shutil 
from config import cfg 
from core.player import Player

class Recorder(Process):
    def __init__(self, status):
        super().__init__()
        self.command = cfg.recorder.command 
        # status
        self.status = status
        self.recording_proc = None 
        # Init player
        self.player = Player(command=cfg.player.command)

    def block_until_recorder_active(self):
        while self.status.value != LISTEN_STATUS.REC_LISTEN:
            time.sleep(0.1)  

    def run(self):
        while True:
            # 由Detector设置status为active后开始录音
            self.block_until_recorder_active()
            # 定义一个长度为3的先进先出队列
            volume_queue = deque(maxlen=2)
            files = [] 
            for i in range(30): # 最少录制3秒，最长说30秒
                subprocess.Popen(args=self.command+["-d","1",f"tmp-{i:02d}.wav"])
                files.append(f"tmp-{i:02d}.wav")
                time.sleep(1) # 等待录完
                # 判断音量
                volume = get_wav_volume(f"tmp-{i:02d}.wav")
                volume_queue.append(volume)
                if i >= 2 and sum(volume_queue) / 3 < 10: # TODO: 程序运行时抓取安静状态下的音量
                    break 
            concat_multi_wav_files(files) # write to tmp-concat.wav
            self.status.value = LISTEN_STATUS.REC_FINISH
            self.player.play(cfg.sounds.endrec)

    def stop(self):
        try:
            self.recording_proc.terminate()
        except Exception as e:
            print(e)
        finally:
            self.status = LISTEN_STATUS.DET_LISTEN
