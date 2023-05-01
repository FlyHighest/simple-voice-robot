import time
from multiprocessing import Value,Process 
import pvporcupine
from pvrecorder import PvRecorder
import logging 
from config import cfg
from utils import LISTEN_STATUS, current_time
from core.player import Player
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Detector(Process):
    """
    唤醒词检测器
    使用picovoice提供的离线唤醒热词监听器，porcupine引擎
    """
    def __init__(self, status:Value) -> None:
        super().__init__()
        self.status = status
        logger.info("Start Detector")
     
        # Create porcupine module
        access_key = cfg.detector.porcupine.access_key
        keyword_paths = cfg.detector.porcupine.keyword_paths
        model_path = cfg.detector.porcupine.model_path
        self.porcupine = pvporcupine.create(
                access_key=access_key,
                model_path=model_path,
                keyword_paths=keyword_paths,
                sensitivities=[cfg.detector.sensitivity ] * len(keyword_paths),
            )
        self.keyword_paths = keyword_paths



        # Init player
        self.player = Player()

    def block_until_recorder_deactive(self):
        while self.status.value not in [LISTEN_STATUS.DET_LISTEN] :
            time.sleep(0.1)  

    def run(self):
        # Init recorder. 如果在init里初始化recorder，start会阻塞，且没有错误提示
        audio_devices = PvRecorder.get_audio_devices()
        # print("PvRecorder detected audio devices:", audio_devices)
        # print(audio_devices.index(cfg.detector.device),len(audio_devices)-1)
        self.recorder = PvRecorder(device_index=audio_devices.index(cfg.detector.device), 
                              frame_length=self.porcupine.frame_length)
        self.recorder.start()
        try:
            while True:
                # logger.info("detector is listening")
                pcm = self.recorder.read()

                result = self.porcupine.process(pcm)
                if result >= 0:
                    kw = self.keyword_paths[result]
                    logger.info(f"Keyword {kw} Detected at time {current_time()}")
                
                    self.recorder.stop()
                    self.player.play(cfg.sounds.wakeup, blocking=True)
                    self.status.value = LISTEN_STATUS.REC_LISTEN
                    # 阻塞程序直到主动聆听状态结束
                    self.block_until_recorder_deactive()

                    self.recorder.start()
                    

        except pvporcupine.PorcupineActivationError as e:
            logger.error("[Porcupine] AccessKey activation error", stack_info=True)
            raise e
        except pvporcupine.PorcupineActivationLimitError as e:
            logger.error(
                f"[Porcupine] AccessKey has reached it's temporary device limit",
                stack_info=True,
            )
            raise e
        except pvporcupine.PorcupineActivationRefusedError as e:
            logger.error(
                "[Porcupine] AccessKey refused", stack_info=True
            )
            raise e
        except pvporcupine.PorcupineActivationThrottledError as e:
            logger.error(
                "[Porcupine] AccessKey has been throttled",
                stack_info=True,
            )
            raise e
        except pvporcupine.PorcupineError as e:
            logger.error("[Porcupine] 初始化 Porcupine 失败", stack_info=True)
            raise e
        except KeyboardInterrupt:
            logger.info("Stopping ...")
     


