from camera import find_available_cameras
from camera import open_cameras
from camera import release_cameras

# CONFIG
camera_num = 2

def main():
    # Setting up cameras
    available_cameras_index = find_available_cameras()
    
    print("[INFO] available cameras", available_cameras_index)
    if (len(available_cameras_index) < camera_num):
        print("[ERROR] Not enough cameras available")
        return
    
    caps = open_cameras(available_cameras_index[:camera_num])

    print("[INFO] Cameras opened")

    # Tracking
    # Close cameras
    release_cameras(caps)
    print("[INFO] Cameras released")

if __name__ == "__main__":
    main()
