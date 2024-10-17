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

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

########## ########## ########## ########## ########## ########## 
# 3Dリアルタイムプロットのセットアップ
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 軸の範囲を設定
ax.set_xlim([-70, 70])
ax.set_ylim([-70, 70])
ax.set_zlim([-70, 70])

# 軸のラベルを設定
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# リアルタイムに更新する座標
tracked_point, = ax.plot([], [], [], 'go', label="Tracked Point")

########## ########## ########## ########## ########## ##########

def main():
    # Setting up cameras
    available_cameras_index = find_available_cameras()

    print("[INFO] available cameras", available_cameras_index)
    if len(available_cameras_index) < CAMERA_NUM:
        print("[ERROR] Not enough cameras available")
        return

    #    cameras = open_cameras(available_cameras_index[:CAMERA_NUM])
    cameras = open_cameras([2, 1])
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

        xyz_coord = convert_2d_to_3d(deg_x_y[0], deg_x_y[1])

        ########## ########## ########## ########## ########## ##########
        # 3D座標が取得できた場合にプロットを更新
        if None not in xyz_coord:
            tracked_point.set_data([xyz_coord[0]], [xyz_coord[1]])
            tracked_point.set_3d_properties([xyz_coord[2]])
            plt.draw()
            plt.pause(0.01)  # プロットの更新速度
        ########## ########## ########## ########## ########## ##########

        # 画像に円を描画して表示
        imgs_show(draw_circle(frames, x_y))

        if is_key_pressed("q"):
            break

    # Close cameras
    release_cameras(cameras)
    print("[INFO] Cameras released")


if __name__ == "__main__":
    main()
