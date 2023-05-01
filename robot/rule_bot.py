from .robot import Robot
import random 
class RuleBot(Robot):
    # 基于规则的，完美匹配时触发

    matched_words = {
            "": ["哎呀，我没听清，可以再说一遍吗","你的声音有点小，我听不清"]
        }

    def __init__(self) -> None:
        super().__init__()


    def reply(self, text):
        return random.choice(self.matched_words[text])