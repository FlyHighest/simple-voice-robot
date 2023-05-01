# 输入文本，分析意图，选择某个robot进行回复

from .openai_bot import OpenAIBot
from .sysinfo_bot import SysInfoBot
class IntentAnalyzer:
    def __init__(self) -> None:
        pass

    def analyze(self, text):
        # 特殊： 汇报本机状态
        if text.startswith("汇报"): 
            return SysInfoBot
        
        # 通用：利用文本相似度解析用户意图

        return OpenAIBot

