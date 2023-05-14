import os
import edge_tts
from utils import convert_mp3_to_wav
from core.player import Player
import asyncio
class EdgeTTS:
    """
    edge-tts 引擎
    voice: 发音人，默认是 zh-CN-XiaoxiaoNeural
        全部发音人列表：命令行执行 edge-tts --list-voices 可以打印所有语音
    """

    SLUG = "edge-tts"

    def __init__(self, voice="zh-CN-YunxiNeural"):
        self.voice = voice
        self.player = Player()

    async def async_get_speech(self, phrase):
        try:
            tmpfile = os.path.join("tmp-tts.mp3")
            tts = edge_tts.Communicate(text=phrase, voice=self.voice, volume="+99%")
            await tts.save(tmpfile)    
            return tmpfile
        except Exception as e:
            print("TTS", e)
            return None

    def text_to_speech(self, phrase):
        event_loop = asyncio.new_event_loop()
        tmpfile = event_loop.run_until_complete(self.async_get_speech(phrase))
        event_loop.close()
        convert_mp3_to_wav("tmp-tts.mp3") 
        self.player.play("tmp-tts.wav",blocking=True)
        # return tmpfile

