import cv2
import numpy as np

def imgs_show(imgs):
    for i, img in enumerate(imgs):
        cv2.imshow(f'Camera {i}', img)

def create_mask(imgs, thresholds):
    masks = []
    for i, img in enumerate(imgs):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        mask = cv2.inRange(hsv_img, thresholds[i]["lower"], thresholds[i]["upper"])  # HSVからマスクを作成
        masks.append(mask)

    return masks

def retrieve_x_y_from_max_contour(masks):
    x_y = []
    for mask in masks:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 輪郭検出

        if len(contours) == 0:
            x_y.append((None, None))
            continue

        largest_contour = max(contours, key=cv2.contourArea)  # 最も大きい輪郭を選択
        M = cv2.moments(largest_contour)

        if M["m00"] == 0:
            x_y.append((None, None))
            print("[ERROR] m00 is 0")
            continue
        
        x = int(M["m10"] / M["m00"])  # 輪郭の重心のx座標を算出
        y = int(M["m01"] / M["m00"])  # 輪郭の重心のy座標を算出

        x_y.append((x, y))

    return x_y

def draw_circle(imgs, x_y):
    for i, (x, y) in enumerate(x_y):
        try:
            cv2.circle(imgs[i], (x, y), 40, (0, 255, 0), 10)  # 重心に円を描画
        except:
            pass

    return imgs
