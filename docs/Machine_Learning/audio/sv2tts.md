

# Audio Mel Spectrogram

理解Mel Spectrogram
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53

- 时域信号：横轴为时间， 纵轴为振幅（-1， 1)
- 频域信号： 快速傅立叶变换（FFT）， 分析时域信号由哪些频率的波构成, 横轴为频率， 纵轴为振幅
- Spectrogram： 横轴为时间， 纵轴为频率， 通过colorbar方式表达振幅
- Mel Scale： 人对频率的感知不是线性的，

信号的频率随着时间由变化，对信号按照时间段分窗进行FFT分析，得到频谱图



Wavenet -> Tacotron

# SV2TTS (Real-Time-Voice-Cloning)

- encoder: 获得表达声音特征的embedding, 3层lstm
- synthesizer: Tacotron
- vocoder: WaveRNN

## speaker verification (SV)  speaker representation
speaker embedding: 表达一个人的音色特征, speaker representation

> encoder（Speaker Encoder） 

输入音频采样率为16000 （每秒16000个采样点） -> Mel Spectrogram -> Speaker Encoder -> speaker embedding

3层lstm
输入： 40维， mel bin数量 
输出： 256维embedding


generalized end-to-end loss(GE2E): 损失函数


- Text dependent speaker verification(TD-SV)：  使用特定文本进行检查
- Text independent speaker verification (TI-SV)： 使用任意文本进行检查




texts and speaker embeddings -> synthesizer -> Mel Spectrogram


## multi-speaker TTS

VCTK 数据集


# librosa

librosa.feature.melspectrogram

- sr: 采样率
- n_fft: 多少个采样点作为一个窗口进行fft
- hop_length: 两个相邻窗口间隔多少个采样点
- n_mels: 频率划分为多少个bin

输入音频： 时长为t秒
输出大小（n_mels, t*sr/hop_length)