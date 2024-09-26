import cv2
import numpy as np
from collections import deque

# 3次元座標を計算する関数
def calculate_3d_coordinates(x1, y1, x2, f, B):
    Z = (f * B) / (x1 - x2)
    X = (x1 * Z) / f
    Y = (y1 * Z) / f
    return X, Y, Z

def contours(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_binary = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None, None
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, None
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    return x, y

# カメラのデバイスID
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

# カメラのパラメータ（焦点距離とカメラ間距離は調整が必要）
f = 800  # 焦点距離（仮定）
B = 10.0  # カメラ間の距離（cm単位）

# ユーザーが選択した原点
origin_selected = False
origin_x1, origin_y1 = None, None
origin_x2, origin_y2 = None, None

while True:
    # 各カメラからフレームを取得
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1 or not ret2:
        print("フレームの取得に失敗しました")
        break

    # 最初にユーザーに原点となる対象物を両カメラで選択させる
    if not origin_selected:
        cv2.putText(frame1, "Select origin (Camera 1) and press ENTER", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame2, "Select origin (Camera 2) and press ENTER", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # カメラ1で原点を選択
        origin_rect1 = cv2.selectROI("Select Origin (Camera 1)", frame1, fromCenter=False, showCrosshair=True)
        origin_x1, origin_y1 = int(origin_rect1[0] + origin_rect1[2] / 2), int(origin_rect1[1] + origin_rect1[3] / 2)
        
        # カメラ2で原点を選択
        origin_rect2 = cv2.selectROI("Select Origin (Camera 2)", frame2, fromCenter=False, showCrosshair=True)
        origin_x2, origin_y2 = int(origin_rect2[0] + origin_rect2[2] / 2), int(origin_rect2[1] + origin_rect2[3] / 2)
        
        origin_selected = True
        cv2.destroyWindow("Select Origin (Camera 1)")
        cv2.destroyWindow("Select Origin (Camera 2)")
        print(f"Origin selected at x1={origin_x1}, y1={origin_y1} (Camera 1)")
        print(f"Origin selected at x2={origin_x2}, y2={origin_y2} (Camera 2)")

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

    if x1 is not None and y1 is not None and x2 is not None:
        # 両カメラで選択した原点を基準に3次元座標を計算
        X, Y, Z = calculate_3d_coordinates(x1 - origin_x1, y1 - origin_y1, x2 - origin_x2, f, B)
        print(f"3D Position relative to origin - X: {X:.2f}, Y: {Y:.2f}, Z: {Z:.2f}")

        # カメラ1に検出結果を描画
        trajectory1.append((x1, y1))
        frame1 = cv2.circle(frame1, (x1, y1), 10, (0, 0, 255), 2)
        # 原点を描画
        frame1 = cv2.circle(frame1, (origin_x1, origin_y1), 10, (255, 0, 0), 2)  # 青で原点表示

        # カメラ2に検出結果を描画
        trajectory2.append((x2, y2))
        frame2 = cv2.circle(frame2, (x2, y2), 10, (0, 0, 255), 2)
        # 原点を描画
        frame2 = cv2.circle(frame2, (origin_x2, origin_y2), 10, (255, 0, 0), 2)  # 青で原点表示

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
