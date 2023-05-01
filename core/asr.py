import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models
from config import cfg
import base64 

class TencentASR:
    def __init__(self) -> None:
        cred = credential.Credential(cfg.api.tencent_secret_id, cfg.api.tencent_secret_key)
        # 实例化要请求产品的client对象
        self.client = asr_client.AsrClient(cred, "")

    def speech_recognize(self, wav_file='tmp-concat.wav'):
        with open(wav_file,"rb") as file:
            content = file.read()
            data_len = len(content)
            data = base64.b64encode(content).decode()
        try:

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.SentenceRecognitionRequest()
            params = {
                "EngSerViceType":"16k_zh",
                "SourceType": 1,
                "SubServiceType": 2,
                "VoiceFormat": "wav",
                "Data":  data,
                "DataLen": data_len,

            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个SentenceRecognitionResponse的实例，与请求对象对应
            resp = self.client.SentenceRecognition(req)
            # 输出json格式的字符串回包
            result = json.loads(resp.to_json_string())['Result']
            return result
        except TencentCloudSDKException as err:
            print(err)
            return ""