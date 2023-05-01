from core import Detector,Recorder,TencentASR,EdgeTTS
from robot import IntentAnalyzer
from multiprocessing import Value 
from utils import LISTEN_STATUS
import time 

if __name__ == "__main__":

    # 模块1: 用户声音监听和录制
    listen_status = Value("i", LISTEN_STATUS.DET_LISTEN)

    detector = Detector(listen_status)
    recorder = Recorder(listen_status)
    
    detector.start()
    recorder.start()

    # 模块2: 语音识别和结果构造
    asr = TencentASR()
    intent_analyzer = IntentAnalyzer()
    tts = EdgeTTS()
    while True:
        while listen_status.value != LISTEN_STATUS.REC_FINISH:
            time.sleep(0.1)
            continue
        text = asr.speech_recognize()

        print("识别:", text)
        robot = intent_analyzer.analyze(text)()
        response_text = robot.reply(text)
        robot.start()

        print("回复:", response_text)
        tts.text_to_speech(response_text)
        listen_status.value = LISTEN_STATUS.DET_LISTEN

    # 模块3: 回复播放


