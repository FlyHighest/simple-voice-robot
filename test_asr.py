from core import TencentASR

asr = TencentASR()
res = asr.speech_recognize("test1.wav")
print(res)