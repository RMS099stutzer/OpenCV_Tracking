import cv2
import numpy

def imgs_show(imgs):
    for i, img in enumerate(imgs):
        cv2.imshow(f'Camera {i}', img)

def create_mask(imgs, lower, upper):
    masks = []
    for img in imgs:
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, lower, upper)
        masks.append(mask)

    return masks