from core import Detector,Recorder,Player
from multiprocessing import Value 
from utils import LISTEN_STATUS

if __name__ == "__main__":
    listen_status = Value("i", LISTEN_STATUS.DET_LISTEN)

    detector = Detector(listen_status)
    recorder = Recorder(listen_status)
    
    detector.start()
    recorder.start()

    detector.join()
    recorder.join()