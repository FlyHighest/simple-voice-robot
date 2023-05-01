from utils import LISTEN_STATUS
import subprocess
import time 
from multiprocessing import Process 
from utils import get_wav_volume,concat_multi_wav_files
from collections import deque
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
        self.player = Player()

        # Detect silent thresh
        tmp_volume_sum = 0
        for i in range(3):
            p = subprocess.Popen(args=self.command+["-d","1",f"tmp-detect.wav"])
            p.wait()
            tmp_volume_sum+=get_wav_volume("tmp-detect.wav")
            
        self.silent_thresh = tmp_volume_sum/3 + 10
        print("Silent Volume Threshold",self.silent_thresh)

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
                print("Volume detected",volume)
                volume_queue.append(volume)
                if i >= 2 and sum(volume_queue) / 3 < self.silent_thresh: # TODO: 程序运行时抓取安静状态下的音量
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
