import wave,os
import numpy as np 
import math 
def concat_multi_wav_files(files):
    # 打开所有的wav文件
    wave_files = []
    for file in files:
        wave_files.append(wave.open(file, 'rb'))
    
    # 创建一个新的wav文件
    output = wave.open('tmp-concat.wav', 'wb')
    output.setparams(wave_files[0].getparams())

    # 逐个写入采样数据
    for wave_file in wave_files:
        output.writeframes(wave_file.readframes(wave_file.getnframes()))

    # 关闭所有的wav文件
    for wave_file,file in zip(wave_files,files):
        wave_file.close()
        os.remove(file)

    output.close()

def get_wav_volume(wav_file):
    with wave.open(wav_file, 'r') as wav:
        # 获取每个采样点的位数
        sample_width = wav.getsampwidth()
        # 读取所有的采样数据
        data = wav.readframes(wav.getnframes())
    # 将二进制采样数据转化为数组格式
    samples = np.frombuffer(data, dtype=f'int{8*sample_width}')
    # 获取音量大小
    volume = np.sqrt(np.mean(np.square(samples)))
    return volume