import subprocess
from config import cfg 
class Player:
    def __init__(self):
        self.command = cfg.player.command 
        # status
        self.playing_proc = None 

    def play(self, file, blocking=False):
        self.playing_proc = subprocess.Popen(self.command+[file])
        if blocking:
            self.playing_proc.wait()

    def stop(self):
        try:
            self.playing_proc.terminate()
        except Exception as e:
            print(e)
    