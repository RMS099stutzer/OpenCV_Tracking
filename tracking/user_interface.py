import os

# カメラの設定
try: 
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
except:
    pass

import cv2

def is_key_pressed(key):
    return cv2.waitKey(1) & 0xFF == ord(key)