import json 
from typing import * 
class AttrDict:
    def __init__(self, d:Union[dict,str,int,float]):
        for k, v in d.items():
            if type(v)==dict:
                self.__setattr__(k, AttrDict(v))
            else:
                self.__setattr__(k, v)

config_json = json.load(open("./config.json"))
cfg = AttrDict(config_json)