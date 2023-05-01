# 输入文本，分析意图，选择某个robot进行回复

from .openai_bot import OpenAIBot
from .sysinfo_bot import SysInfoBot
from .rule_bot import RuleBot
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentAnalyzer:
    def __init__(self) -> None:
        pass

    def analyze(self, text):
        # 特殊： 没有识别到内容
        if text in RuleBot.matched_words:
            logger.info("RuleBot")
            return RuleBot
        
        # 特殊： 汇报本机状态
        if text.startswith("汇报"): 
            logger.info("SysInfoBot")
            return SysInfoBot
        
        # 通用：利用文本相似度解析用户意图
        # TODO

        # 兜底：chatgpt
        logger.info("OpenAIBot")
        return OpenAIBot

