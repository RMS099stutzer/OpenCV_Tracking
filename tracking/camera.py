import os

# カメラの設定
try: 
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
except:
    pass

import cv2

def find_available_cameras():
    max_index = 10
    available_cameras_index = []

    for i in range(max_index):
        try:
            cap = cv2.VideoCapture(i)
            ret = cap.isOpened()
            cap.release()

            if ret:
                print(f"Camera index {i} is available")
                available_cameras_index.append(i)
        except:
            # Camera not available
            pass
    
    return available_cameras_index

def open_cameras(index):
    cameras = []
    for i in index:
        cap = cv2.VideoCapture(i)
        cameras.append(cap)
    
    return cameras

def release_cameras(cameras):
    for cap in cameras:
        cap.release()

def retrieve_frames(cameras):
    frames = []
    for camera in cameras:
        couldRead, frame = camera.read()
        
        if couldRead:
            frames.append(frame)
        else:
            frames.append(None)
            print("[ERROR] Could not read frame from camera")
    
    return frames