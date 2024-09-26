import cv2
import numpy as np
from collections import deque

def contours(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # グレースケール化
    ret, img_binary = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)  # 二値化
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 輪郭検出
    if len(contours) == 0:
        return None, None  # 輪郭が見つからない場合
    largest_contour = max(contours, key=cv2.contourArea)  # 最も大きい輪郭を選択
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, None  # 面積がゼロの場合
    x = int(M["m10"] / M["m00"])  # 輪郭の重心のx座標を算出
    y = int(M["m01"] / M["m00"])  # 輪郭の重心のy座標を算出
    return x, y

# カメラのデバイスIDを指定（通常、0が1台目、1が2台目）
cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)

if not cam1.isOpened() or not cam2.isOpened():
    print("カメラの接続に失敗しました")
    exit()

# 白色の閾値設定（HSV色空間、色、彩度、明るさ）
lower = np.array([0, 0, 200])
upper = np.array([180, 20, 255])

# 軌跡を保存するためのデック（最大長さ500）
trajectory1 = deque(maxlen=500)
trajectory2 = deque(maxlen=500)

while True:
    # 各カメラからフレームを取得
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1 or not ret2:
        print("フレームの取得に失敗しました")
        break

    # フレームをHSV色空間に変換
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    # マスクを作成
    frame_mask1 = cv2.inRange(hsv1, lower, upper)
    frame_mask2 = cv2.inRange(hsv2, lower, upper)

    # マスクを適用
    filtered1 = cv2.bitwise_and(frame1, frame1, mask=frame_mask1)
    filtered2 = cv2.bitwise_and(frame2, frame2, mask=frame_mask2)

    # 輪郭検出
    x1, y1 = contours(filtered1)
    x2, y2 = contours(filtered2)

    if x1 is not None and y1 is not None:
        trajectory1.append((x1, y1))
        frame1 = cv2.circle(frame1, (x1, y1), 10, (0, 0, 255), 2)  # 検出した位置にサークル描画
        print(f"Camera 1 - Object position: x={x1}, y={y1}")

    if x2 is not None and y2 is not None:
        trajectory2.append((x2, y2))
        frame2 = cv2.circle(frame2, (x2, y2), 10, (0, 0, 255), 2)  # 検出した位置にサークル描画
        print(f"Camera 2 - Object position: x={x2}, y={y2}")

    # 軌跡を描画
    for i in range(1, len(trajectory1)):
        if trajectory1[i - 1] is None or trajectory1[i] is None:
            continue
        cv2.line(frame1, trajectory1[i - 1], trajectory1[i], (0, 255, 0), 2)

    for i in range(1, len(trajectory2)):
        if trajectory2[i - 1] is None or trajectory2[i] is None:
            continue
        cv2.line(frame2, trajectory2[i - 1], trajectory2[i], (0, 255, 0), 2)

    # フレームをウィンドウに表示
    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# カメラとウィンドウを解放
cam1.release()
cam2.release()
cv2.destroyAllWindows()
