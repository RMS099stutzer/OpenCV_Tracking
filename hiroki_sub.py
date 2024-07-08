import cv2
import numpy as np
from matplotlib import pyplot as plt

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

x_list = []
y_list = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_mask = cv2.inRange(hsv, lower, upper)
    filtered = cv2.bitwise_and(frame, frame, mask=frame_mask)

    x, y = contours(filtered)
    if x is not None and y is not None:
        frame = cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)  # 検出した位置にサークル描画
        x_list.append(x)
        y_list.append(y)

    cv2.imshow("Webcam Live", frame)  # 画面表示

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# ここからグラフ描画
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')

ax1.set_xlim(0, max(x_list) if x_list else 800)
ax1.set_ylim(0, max(y_list) if y_list else 400)

ax1.set_xlabel('x')
ax1.set_ylabel('y')

ax1.scatter(x_list, y_list, label='Tracking result')
plt.legend()
fig.tight_layout()

plt.show()
plt.close()
