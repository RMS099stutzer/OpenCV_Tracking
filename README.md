# OpenCV_Tracking

OpenCVを使って3Dトラッキングをしていき！！！


## 環境構築

pyenvで3.10.5環境を用意してます。モジュールはrequirements.txtでインストールしてね。

```
% pyenv install 3.10.5
% python -V
3.10.5
```

```
% pip install -r requirements.txt
```

## 進捗

### 2024/07/08

- 2値化された動画から位置をトラッキングしてplotできる（video_tracking_hiroki.py）
- カメラのキャプチャを2値化できた（realtime_camera_capture.py）

**次やること**

- とりあえずカメラからリアルタイムでトラッキングしよう
- video_r.mp4だとエラーが出た原因を明確にしよう（容量問題？3MBだとできるらしい…？）

```sh
% python video_tracking_hiroki.py
Traceback (most recent call last):
  File "/Users/shirokuma89dev/GitHub/OpenCV_Tracking/video_tracking_hiroki.py", line 38, in <module>
    x, y = contours(frame)                                            # 輪郭検出から物体中心を算出
  File "/Users/shirokuma89dev/GitHub/OpenCV_Tracking/video_tracking_hiroki.py", line 14, in contours
    contours = np.array(contours)                                     # 輪郭情報をndarrayに変換
ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (422,) + inhomogeneous part.
```

### 2024/07/29

- 2台のカメラそれぞれで座標を取得できた

**次やること**

- カメラのキャリブレーションをやろう
- xy，yz座標を配列に格納しよう
- pc→pcの通信どうするか決めよう