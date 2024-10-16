import numpy as np

# CONFIG
CAMERA_NUM = 1
TRACKING_THRESHOLDS = [
    {
        "lower": np.array([65, 153, 127]),
        "upper": np.array([153, 215, 190]),
    },
    {
        "lower": np.array([67, 99, 59]),
        "upper": np.array([155, 163, 125]),
    },
]
