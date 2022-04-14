

# 人脸检测

- mtcnn 人脸检测
- facenet 人脸特征抽取


# OpenFaceSwap

输入： 两个视频source video and target video， 输出：交换两个视频中的特定人脸

source video
- 用ffmpeg将视频抽取成多个图片
- 每个图片提取得到人脸
```
python\scripts\python.bat faceswap\faceswap.py extract -i E:\workspace\deepfakes\chigua\huaqiang\img -o E:\workspace\deepfakes\chigua\huaqiang\face -D cnn
```

# 人脸交换

给定目标人脸图像
- 对视频的每帧图像进行人脸检测和识别


人脸转换模型




