from .robot import Robot
import openai 
from config import cfg
from multiprocessing import Queue , Process
from collections import deque 

openai.api_key = cfg.api.openai_key
openai.api_base = cfg.api.openai_base

def generate_response(text, history, q):
    print(history)
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system",  "content":"你是家用智能音箱上的语音助手，你的回答简短、准确，且富有幽默感" },
                *history,
                {"role": "user", "content": text},
            ],
        temperature=0.5,
        n=1,
        max_tokens=200,
        user="1"
    )
    content = res['choices'][0]['message']['content']
    q.put(content)
    

class OpenAIBot(Robot):
    history = deque(maxlen=4) # 最多保存2轮对话作为上下文

    def __init__(self) -> None:
        super().__init__()



    def reply(self,text):
        q = Queue(maxsize=1)
        p = Process(target=generate_response,args=(text,self.history, q))
        p.start()
        try:
            response = q.get(timeout=10)
            self.history.append({"role":"user","content":text})
            self.history.append({"role":"assistant","content":response})
        except Exception as e:
            response = "抱歉，出现网络异常，再说一遍好吗"

        return response


    
    