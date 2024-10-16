import numpy as np

CAMERA_X_RANGE = 88 
CAMERA_X_RESOLUTION = 1920
CAMERA_Y_RESOLUTION = 1080
CAMERA_Y_RANGE = (CAMERA_X_RANGE / CAMERA_X_RESOLUTION) * CAMERA_Y_RESOLUTION

def x_y_to_degree(x_y):
    deg_x_y = []

    for i, (x, y) in enumerate(x_y):
        width, height = CAMERA_X_RESOLUTION, CAMERA_Y_RESOLUTION
        
        if x is None or y is None:
            deg_x_y.append((None, None))
            continue

        x, y = x - width / 2, height / 2 - y
        x_degree = (x / width) * CAMERA_X_RANGE
        y_degree = (y / height) * CAMERA_Y_RANGE

        deg_x_y.append((x_degree, y_degree))
    
    return deg_x_y
    
if __name__ == "__main__":
    print(CAMERA_Y_RANGE)