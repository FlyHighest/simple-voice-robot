# 输入文本，分析意图，选择某个robot进行回复

from .openai_bot import OpenAIBot
from .sysinfo_bot import SysInfoBot
from .rule_bot import RuleBot
from .weather_bot import WeatherBot
from pytextclassifier import ClassicClassifier

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentAnalyzer:
    def __init__(self) -> None:
        self.text_classifier = ClassicClassifier(model_dir='statics/intent_svm_classifier', model_name_or_model='svm')
        self.text_classifier.load_model()


    def analyze(self, text):
        # 特殊： 没有识别到内容
        if text in RuleBot.matched_words:
            logger.info("RuleBot")
            return RuleBot
        
        # 特殊： 汇报本机状态
        if text.startswith("汇报"): 
            logger.info("SysInfoBot")
            return SysInfoBot
        
        # 通用：利用文本分类确定用户意图
        predict_label, predict_proba = self.text_classifier.predict([text])
        predict_label = predict_label[0]
        predict_proba = predict_proba[0]
        if predict_proba > 0.9:
            if predict_label=="weather":
                logger.info("WeatherBot")
                return WeatherBot
            elif predict_label=="Reminder":
                return OpenAIBot # TODO


        # 兜底：chatgpt
        logger.info("OpenAIBot")
        return OpenAIBot

