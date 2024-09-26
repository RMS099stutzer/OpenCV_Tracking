import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# 閾値を変えてね（HSV色空間、色、彩度、明るさ）
lower = np.array([0, 0, 0])
upper = np.array([255, 255, 100])

# 2値化を無効化
disable = False

if cap.isOpened() == False:
    print("❌ Cannot open camera")
    exit()

if cap.isOpened():
    print("✅ VideoCapture is opened!")
    print("Width: " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("Height: " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("FPS: " + str(cap.get(cv2.CAP_PROP_FPS)))

    print("Press 'q' to quit")

while cap.isOpened():  # カメラが存在しますか？
    ret, frame = cap.read()
    if ret == True:
        if not disable:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame_mask = cv2.inRange(hsv, lower, upper)

            filtered = cv2.bitwise_and(frame, frame, mask=frame_mask)

        # frame_mask: 2値化した画像
        # frame: 元画像
        # filtered: マスクをかけた画像

        cv2.imshow("Webcam Live", frame_mask) #画面表示

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
