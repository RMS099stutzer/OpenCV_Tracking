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

cap = cv2.VideoCapture(0)

# 白色の閾値設定（HSV色空間、色、彩度、明るさ）
lower = np.array([0, 0, 200])
upper = np.array([180, 20, 255])

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

print("✅ VideoCapture is opened!")
print("Width: " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("Height: " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print("FPS: " + str(cap.get(cv2.CAP_PROP_FPS)))

print("Press 'q' to quit")

# 軌跡を保存するためのデック（最大長さ500）
trajectory = deque(maxlen=500)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_mask = cv2.inRange(hsv, lower, upper)
    filtered = cv2.bitwise_and(frame, frame, mask=frame_mask)

    x, y = contours(filtered)
    if x is not None and y is not None:
        trajectory.append((x, y))
        frame = cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)  # 検出した位置にサークル描画

        # 座標を出力
        print(f"Object position: x={x}, y={y}")

    # 軌跡を描画
    for i in range(1, len(trajectory)):
        if trajectory[i - 1] is None or trajectory[i] is None:
            continue
        cv2.line(frame, trajectory[i - 1], trajectory[i], (0, 255, 0), 2)

    cv2.imshow("Webcam Live", frame)  # 画面表示

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
