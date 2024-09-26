import cv2

device_index = 2  # 使用するデバイスのインデックス
cap = cv2.VideoCapture(device_index)

if cap.isOpened():
    # 解像度の取得
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Device {device_index}:")
    print(f"  Resolution: {width} x {height}")
    print(f"  FPS: {fps}")

    cap.release()
else:
    print(f"Device {device_index} is not available.")

