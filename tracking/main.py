import numpy as np

from camera import find_available_cameras
from camera import open_cameras
from camera import release_cameras
from camera import retrieve_frames

from image import imgs_show

from user_interface import is_key_pressed 

# CONFIG
camera_num = 2

def main():
    # Setting up cameras
    available_cameras_index = find_available_cameras()
    
    print("[INFO] available cameras", available_cameras_index)
    if (len(available_cameras_index) < camera_num):
        print("[ERROR] Not enough cameras available")
        return
    
    cameras = open_cameras(available_cameras_index[:camera_num])
    print("[INFO] Cameras opened")

    # Tracking
    input("[INFO] Press Enter to start tracking")

    while True:
        frames = retrieve_frames(cameras)
        
        if np.any([frame is None for frame in frames]):
            print("[ERROR] Could not read frame from camera")
            break
        
        imgs_show(frames)

        if is_key_pressed('q'):
            break

    # Close cameras
    release_cameras(cameras)
    print("[INFO] Cameras released")

if __name__ == "__main__":
    main()
