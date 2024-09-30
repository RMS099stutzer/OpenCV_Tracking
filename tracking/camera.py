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
            # print(f"Camera index {i} is not available")
            pass
    
    return available_cameras_index

def open_cameras(index):
    caps = []
    for i in index:
        cap = cv2.VideoCapture(i)
        caps.append(cap)
    
    return caps

def release_cameras(caps):
    for cap in caps:
        cap.release()