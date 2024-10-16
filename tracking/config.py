import numpy as np

# CONFIG
CAMERA_NUM = 2
TRACKING_THRESHOLDS = [
    {
        "lower": np.array([240, 100, 100]),
        "upper": np.array([255, 160, 160]),
    },
    {
        "lower": np.array([240, 100, 100]),
        "upper": np.array([255, 160, 160]),
    },
]

