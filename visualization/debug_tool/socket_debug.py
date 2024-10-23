import socket  # ソケット通信
import matplotlib.pyplot as plt
import numpy as np
import time  # 時間

z = np.arange(0, 20, 0.5)
x = np.cos(z)
y = np.sin(z)

host = "10.101.224.180"  # Processingで立ち上げたサーバのIPアドレス
port = 10001  # Processingで設定したポート番号

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # オブジェクトの作成
socket_client.connect((host, port))  # サーバに接続

# socket_client.send('送信するメッセージ') ←これでprocessing側に送信(0.07秒くらい遅らせてほしい)
# ここからはprocessing動作確認様用なので考えなくていいです
for i in np.arange(0.0, 20.0, 0.5):
    print(
        "FFFF,"
        + str(i * 10)
        + ","
        + str(round(np.sin(i), 3) * 100 + 150)
        + ","
        + str(round(np.cos(i), 3) * 100 + 150)
    )
    socket_client.send(
        (
            "FFFF,"
            + str(i * 10)
            + ","
            + str(round(np.sin(i), 3) * 100 + 150)
            + ","
            + str(round(np.cos(i), 3) * 100 + 150)
        ).encode("utf-8")
    )
    time.sleep(0.07)

socket_client.send(
    (
        "FFFF,"
        + str(200)
        + ","
        + str(round(np.sin(20), 3) * 100 + 150)
        + ","
        + str(round(np.cos(20), 3) * 100 + 150)
    ).encode("utf-8")
)
time.sleep(0.07)
socket_client.send(
    ("AAAA," + str(1) + "," + str(1) + "," + str(1)).encode("utf-8")
)  # AAAAの後は適当な数字でいい
time.sleep(0.07)
for i in np.arange(0.0, 20.0, 0.5):
    print(
        "FFFF,"
        + str(i * 10)
        + ","
        + str(round(np.cos(i), 3) * 100 + 150)
        + ","
        + str(round(np.sin(i), 3) * 100 + 150)
    )
    socket_client.send(
        (
            "FFFF,"
            + str(round(np.cos(i), 3) * 100 + 150)
            + ","
            + str(round(np.sin(i), 3) * 100 + 150)
            + ","
            + str(i * 10)
        ).encode("utf-8")
    )
    time.sleep(0.07)
socket_client.send(
    (
        "1111,"
        + str(round(np.cos(20), 3) * 100 + 150)
        + ","
        + str(round(np.sin(20), 3) * 100 + 150)
        + ","
        + str(200)
    ).encode("utf-8")
)
socket_client.close()
