import numpy as np

# default config
CAMERA_X_RANGE = 88
CAMERA_X_RESOLUTION = 640
CAMERA_Y_RESOLUTION = 480
CAMERA_Y_RANGE = (CAMERA_X_RANGE / CAMERA_X_RESOLUTION) * CAMERA_Y_RESOLUTION

CAMERA_TOP_POS = {"x": 0, "y": 0, "z": 150}
CAMERA_LEFT_POS = {"x": -190, "y": 0, "z": 0}


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


def convert_2d_to_3d(top_deg_xy, left_deg_xy):
    # Noneがある場合はNoneを返す
    if None in top_deg_xy or None in left_deg_xy:
        return (None, None, None)

    # 上のカメラの三次元の線形方程式を出します
    # p = a + td_vec
    a = [CAMERA_TOP_POS["x"], CAMERA_TOP_POS["y"], CAMERA_TOP_POS["z"]]

    d_vec = np.array([0.0, 0.0, -1.0])
    
    # Rotate around the x-axis
    theta_x = np.deg2rad(top_deg_xy[1])
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, np.cos(theta_x), np.sin(theta_x)],
        [0, -np.sin(theta_x), np.cos(theta_x)]
    ])
    d_vec = rotation_matrix_x @ d_vec

    # Rotate around the y-axis
    theta_y = np.deg2rad(top_deg_xy[0])
    rotation_matrix_y = np.array([
        [np.cos(theta_y), 0, np.sin(theta_y)],
        [0, 1, 0],
        [-np.sin(theta_y), 0, np.cos(theta_y)]
    ])
    d_vec = rotation_matrix_y @ d_vec

    d_vec = d_vec.tolist()

    print(d_vec)


if __name__ == "__main__":
    print(CAMERA_Y_RANGE)
