# #グレースケール化と二値化

# import cv2
 
# # 動画読み込みの設定
# movie = cv2.VideoCapture('video_r.mp4')
 
# # 動画ファイル保存用の設定
# fps = int(movie.get(cv2.CAP_PROP_FPS))                         # 動画のFPSを取得
# w = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))                   # 動画の横幅を取得
# h = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))                  # 動画の縦幅を取得
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')            # 動画保存時のfourcc設定（mp4用）
# video = cv2.VideoWriter('video_out_r.mp4', fourcc, fps, (w, h), False)  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
 
# # 背景差分の設定
# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()              # 背景オブジェクトを作成
 
# # ファイルからフレームを1枚ずつ取得して動画処理後に保存する
# while True:
#     ret, frame = movie.read()                                  # フレームを取得
#     fgmask = fgbg.apply(frame)                                 # 前景領域のマスクを取得する
#     video.write(fgmask)                                        # 動画を保存する
 
#     # フレームが取得できない場合はループを抜ける
#     if not ret:
#         break
 
# # 撮影用オブジェクトとウィンドウの解放
# movie.release()




import numpy as np
import cv2
from matplotlib import pyplot as plt
 
# 画像から輪郭を検出する関数
def contours(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                  # グレースケール化
    ret, img_binary = cv2.threshold(img_gray,                         # 二値化
                                    60, 255,                          # 二値化のための閾値60(調整要)
                                    cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_binary,                # 輪郭検出
                                           cv2.RETR_EXTERNAL,         # 外側の輪郭のみ抽出
                                           cv2.CHAIN_APPROX_SIMPLE)
    contours = np.array(contours)                                     # 輪郭情報をndarrayに変換
    x = np.mean(contours[0].T[0, 0])                                  # 輪郭のx方向平均値を算出
    y = np.mean(contours[0].T[1, 0])                                  # 輪郭のy方向平均値を算出
    return x, y
 
movie = cv2.VideoCapture('video_r.mp4')                                 # 動画ファイルの読み込み
 
# 動画ファイル保存用の設定
fps = int(movie.get(cv2.CAP_PROP_FPS))                                # 動画のFPSを取得
w = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))                          # 動画の横幅を取得
h = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))                         # 動画の縦幅を取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')                   # 動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('video_out_r.mp4', fourcc, fps, (w, h), True)   # 動画の仕様（ファイル名、fourcc, FPS, サイズ, カラー）
 
# ファイルからフレームを1枚ずつ取得して動画処理後に保存する
x_list = []
y_list = []
while True:
    ret, frame = movie.read()                                         # フレームを取得
 
    # フレームが取得できない場合はループを抜ける
    if not ret:
        break
 
    x, y = contours(frame)                                            # 輪郭検出から物体中心を算出
 
    frame = cv2.circle(frame, (int(x), int(y)), 30, (0, 255, 0), 3)   # 検出した位置にサークル描画
 
    video.write(frame)  # 動画を保存する
    x_list.append(x)
    y_list.append(y)
 
# 動画オブジェクト解放
movie.release()

# ここからグラフ描画
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')

# スケール設定
ax1.set_xlim(0, 800)
ax1.set_ylim(0, 400)

# 軸のラベルを設定する。
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# データプロット
ax1.scatter(x_list, y_list, label='Tracking result')
plt.legend()
fig.tight_layout()

# グラフを表示する。
plt.show()
plt.close()