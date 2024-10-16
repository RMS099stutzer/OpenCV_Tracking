import os

# カメラの設定
try: 
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
except:
    pass

import cv2
import numpy as np

from config import CAMERA_NUM
from config import TRACKING_THRESHOLDS

from camera import find_available_cameras
from camera import open_cameras
from camera import release_cameras
from camera import retrieve_frames

from image import imgs_show
from image import create_mask
from image import retrieve_x_y_from_max_contour
from image import draw_circle
from image import draw_black_rect

from multi_image_to_3d import x_y_to_degree
from multi_image_to_3d import convert_2d_to_3d

from user_interface import is_key_pressed

def main():
    # Setting up cameras
    available_cameras_index = find_available_cameras()

    print("[INFO] available cameras", available_cameras_index)
    if len(available_cameras_index) < CAMERA_NUM:
        print("[ERROR] Not enough cameras available")
        return

#    cameras = open_cameras(available_cameras_index[:CAMERA_NUM])
    cameras = open_cameras([1, 2])
    print("[INFO] Cameras opened")
    
    # show the resolution of the camera
    for i, camera in enumerate(cameras):
        width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"[INFO] Camera {i} resolution: {width}x{height}")

    # Tracking
    input("[INFO] Press Enter to start tracking")

    print("[INFO] Tracking started")
    print("[INFO] Press 'q' to stop tracking")

    while True:
        frames = retrieve_frames(cameras)

        if np.any([frame is None for frame in frames]):
            print("[ERROR] Could not read frame from camera")
            break

        # Create mask
        frames[1] = draw_black_rect(frames[1], (550, 0), (640, 480))
        masks = create_mask(frames, TRACKING_THRESHOLDS)
        x_y = retrieve_x_y_from_max_contour(masks)
        deg_x_y = x_y_to_degree(x_y)

        convert_2d_to_3d(deg_x_y[0], deg_x_y[1])

        # print("[INFO] 座標", x_y, "\t角度", deg_x_y)
        imgs_show(draw_circle(frames, x_y))

        if is_key_pressed("q"):
            break

    # Close cameras
    release_cameras(cameras)
    print("[INFO] Cameras released")


if __name__ == "__main__":
    main()
