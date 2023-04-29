import subprocess

class Player:
    def __init__(self, command=["aplay","-D","sysdefault:CARD=Device"]):
        self.command = command 
        # status
        self.playing_proc = None 

    def play(self, file):
        self.playing_proc = subprocess.Popen(self.command+[file])

    def stop(self):
        try:
            self.playing_proc.terminate()
        except Exception as e:
            print(e)
    