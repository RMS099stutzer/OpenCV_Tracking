import cv2
import numpy as np

def contours(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_binary = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None, None
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None, None
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    return x, y

# カメラのデバイスIDを指定
cam1 = cv2.VideoCapture(0)  # カメラ1
cam2 = cv2.VideoCapture(1)  # カメラ2

if not cam1.isOpened() or not cam2.isOpened():
    print("カメラの接続に失敗しました")
    exit()

# カメラの解像度を取得
width1 = int(cam1.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(cam1.get(cv2.CAP_PROP_FRAME_HEIGHT))
width2 = int(cam2.get(cv2.CAP_PROP_FRAME_WIDTH))
height2 = int(cam2.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 画面の中心点を計算
center_x1, center_y1 = width1 // 2, height1 // 2
center_x2, center_y2 = width2 // 2, height2 // 2

# 白色の閾値設定（HSV色空間）
lower = np.array([0, 0, 200])
upper = np.array([180, 20, 255])

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1 or not ret2:
        print("フレームの取得に失敗しました")
        break

    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    frame_mask1 = cv2.inRange(hsv1, lower, upper)
    frame_mask2 = cv2.inRange(hsv2, lower, upper)

    filtered1 = cv2.bitwise_and(frame1, frame1, mask=frame_mask1)
    filtered2 = cv2.bitwise_and(frame2, frame2, mask=frame_mask2)

    # カメラ1からXY座標を取得
    x1, y1 = contours(filtered1)

    # カメラ2からYZ座標を取得
    y2, z2 = contours(filtered2)

    if x1 is not None and y1 is not None and y2 is not None and z2 is not None:
        # カメラの中心からの相対位置に変換
        x_relative = x1 - center_x1
        y_relative = -(y1 - center_y1)  # y座標の正負を反転
        z_relative = -(z2 - center_y2)  # z座標の正負を反転

        print(f"3D座標: x={x_relative}, y={y_relative}, z={z_relative}")

        # 画面に相対座標を表示
        cv2.putText(frame1, f"3D Position: X={x_relative}, Y={y_relative}, Z={z_relative}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame2, f"3D Position: X={x_relative}, Y={y_relative}, Z={z_relative}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 赤い円で物体の位置を強調表示（トラッキング用）
        frame1 = cv2.circle(frame1, (x1, y1), 10, (0, 0, 255), 2)
        frame2 = cv2.circle(frame2, (y2, z2), 10, (0, 0, 255), 2)

    # カメラ1とカメラ2の映像をそれぞれ表示
    cv2.imshow('Camera 1 - XY', frame1)
    cv2.imshow('Camera 2 - YZ', frame2)

    # 'q'キーでループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam1.release()
cam2.release()
cv2.destroyAllWindows()

#右ポートがxy(カメラ1)，左ポートはyz(カメラ2)