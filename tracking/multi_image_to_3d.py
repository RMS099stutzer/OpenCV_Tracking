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
    top_a = np.array([CAMERA_TOP_POS["x"], CAMERA_TOP_POS["y"], CAMERA_TOP_POS["z"]])
    top_d_vec = np.array([0.0, 0.0, -1.0])  # 上カメラの初期方向ベクトル

    # 上カメラの回転 (x軸周り)
    theta_x = np.deg2rad(top_deg_xy[1])
    rotation_matrix_x = np.array(
        [
            [1, 0, 0],
            [0, np.cos(theta_x), np.sin(theta_x)],
            [0, -np.sin(theta_x), np.cos(theta_x)],
        ]
    )
    top_d_vec = rotation_matrix_x @ top_d_vec

    # 上カメラの回転 (y軸周り)
    theta_y = np.deg2rad(top_deg_xy[0])
    rotation_matrix_y = np.array(
        [
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)],
        ]
    )
    top_d_vec = rotation_matrix_y @ top_d_vec
    top_d_vec = top_d_vec.tolist()

    # 左のカメラのy角度から平面の方程式を算出
    left_a = np.array(
        [CAMERA_LEFT_POS["x"], CAMERA_LEFT_POS["y"], CAMERA_LEFT_POS["z"]]
    )
    left_vec = np.array([1.0, 0.0, 0.0])  # 左カメラの初期法線ベクトル

    # 左カメラの回転 (y軸周り)
    theta_y = np.deg2rad(left_deg_xy[1] + 90)  # 法線ベクトルの調整
    rotation_matrix_y = np.array(
        [
            [np.cos(theta_y), 0, -np.sin(theta_y)],
            [0, 1, 0],
            [np.sin(theta_y), 0, np.cos(theta_y)],
        ]
    )
    left_vec = rotation_matrix_y @ left_vec
    left_vec = left_vec.tolist()  # 法線ベクトル

    # 平面の方程式の係数を求める
    # 平面方程式: left_vec[0] * (x - left_a[0]) + left_vec[1] * (y - left_a[1]) + left_vec[2] * (z - left_a[2]) = 0
    # これを展開すると: left_vec[0]*x + left_vec[1]*y + left_vec[2]*z = D
    D = left_vec[0] * left_a[0] + left_vec[1] * left_a[1] + left_vec[2] * left_a[2]

    # 上カメラの直線方程式: p = top_a + t * top_d_vec
    # これを平面に代入してtを解く
    top_d_vec = np.array(top_d_vec)
    t_numerator = D - np.dot(left_vec, top_a)
    t_denominator = np.dot(left_vec, top_d_vec)

    if t_denominator == 0:
        # 直線が平面に平行で交点がない場合
        return (None, None, None)

    t = t_numerator / t_denominator

    # tを使って上カメラの直線上の点を求める
    intersection_point = top_a + t * top_d_vec

    # print(intersection_point)

    return intersection_point


if __name__ == "__main__":
    print(CAMERA_Y_RANGE)
