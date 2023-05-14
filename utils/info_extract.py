import hanlp 
from .timeparser import timeparser as TP
import datetime 
import pytz 
from config import cfg 
from typing import Union

tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
pos = hanlp.load(hanlp.pretrained.pos.PKU_POS_ELECTRA_SMALL)

def to_iso_time(string):
    # timeparser库的时间字符串转换为iso格式字符串，并且与和风天气接口的时间格式对齐
    dt = datetime.datetime.strptime(string,"%Y-%m-%d %H:%M:%S")
    iso_time_str = dt.astimezone(pytz.timezone('Asia/Shanghai')).isoformat('T',timespec="minutes")
    return iso_time_str

def extract_location(string):
    # PKU词性标注的结果中，ns代表地点。提取文本中出现的最后一个地点名词。
    tok_res = tok(string)
    pos_res = pos(tok_res)
    loc = None 
    for i in range(len(pos_res)):
        if pos_res[i]=="ns":
            loc = tok_res[i]
    return loc or cfg.settings.location

def extract_time(string) -> Union[list,str]:
    # ISO time string or "now". Return a list. [开始时间，结束时间]
    try:
        res = TP.parse_time(string)
        if res['type']=="time_point": 
            # 非周期性的时间
            res_time = map(to_iso_time, res['time'])
            return res_time
        else:
            # TODO: handle time_period type
            return "now" 

    except Exception as e:
        print("Time parse failed",e)
        return "now"
