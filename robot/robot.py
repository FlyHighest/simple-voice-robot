from multiprocessing import Process 

class Robot(Process):
    def __init__(self) -> None:
        super().__init__()
        pass

    def reply(self,text):
        # 这里立即返回一句话
        return text 
    
    def run(self):
        # 新开进程处理耗时程序
        pass 
