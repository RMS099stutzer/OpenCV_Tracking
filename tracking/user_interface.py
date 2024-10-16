import cv2

def is_key_pressed(key):
    return cv2.waitKey(1) & 0xFF == ord(key)