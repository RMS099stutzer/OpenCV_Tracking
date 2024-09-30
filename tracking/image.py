import cv2
import numpy

def imgs_show(imgs):
    for i, img in enumerate(imgs):
        cv2.imshow(f'Camera {i}', img)