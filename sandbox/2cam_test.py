import cv2

# カメラのデバイスIDを指定（通常、0が1台目、1が2台目）
cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)

if not cam1.isOpened() or not cam2.isOpened():
    print("カメラの接続に失敗しました")
    exit()

while True:
    # 各カメラからフレームを取得
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1 or not ret2:
        print("フレームの取得に失敗しました")
        break

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
