from enum import IntEnum

class LISTEN_STATUS(IntEnum):
    REC_LISTEN = 0    # Recorder录制用户声音
    DET_LISTEN = 1  # Detector监听唤醒词
    REC_FINISH = 2  # Recorder录制结束，音频文件保存完毕
