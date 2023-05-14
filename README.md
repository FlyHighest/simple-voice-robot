# 简单的语音助手

整体架构参考[wukong-robot](https://github.com/wzpan/wukong-robot)，做了很大简化。

## 简介 

1. 输入输出部分

Detector(监听唤醒词) -> Recorder(录制用户语音) -> Player(播放回复)

用一个状态值（`listen_status`）来调节Detector和Recorder的工作，录制和播放回复时不进行监听。

Detector使用picovoice提供的离线唤醒热词监听器，porcupine引擎。

Recoder和Player均调用linux系统指令实现。

2. 回复语音构造

ASR(语音识别) -> 意图理解(文本分类) -> Robot(构造回复文本) -> TTS(转语音)

ASR调用腾讯云接口；
意图理解部分使用一个规则+文本分类，识别到用户不同的意图调用不同的Robot类构造回复。文本分类使用[pytextclassifier](https://github.com/shibing624/pytextclassifier)库完成；
TTS使用[edge-tts](https://github.com/rany2/edge-tts)。

目前实现了以下几种Robot：

- RuleBot: 用规则匹配文本内容，处理特殊命令，比如空文本。
- SysInfoBot: 汇报机器状态，如IP、时间、CPU温度等。
- WeatherBot: 天气查询。利用[hanlp](https://github.com/hankcs/HanLP)的词性分析工具提取文本中的地点；利用[timeparser](https://github.com/yujunhuics/timeparser)库提取文本中的时间；调[和风天气API](https://dev.qweather.com/docs/start/)查询天气。
- OpenAIBot: 调OpenAI的ChatCompletion接口。

## 运行

在config.py里写好配置，然后

```sh
python main.py
```

运行后会先录制3秒语音，判断环境声音，动态设置停止录音的音量阈值。