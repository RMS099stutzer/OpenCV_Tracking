import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tracking'))

# tracking/main.py
from tracking.main import tracking_process, data_send_process

# socket_com/sender.py
from socket_com.sender import monitor_folder

import threading

CAMERAS_INDEX = [2, 1]
FOLDER_PATH = r"./visualization/csv"  # 監視するフォルダのパスを記入
SERVER_HOST = "169.254.44.200"  # server側のIPアドレスに置き換える
SERVER_PORT = 6000  # ポート番号

MY_IP = "127.0.0.1"
MY_PORT = 10001

if __name__ == "__main__":
    tracking_thread = threading.Thread(target=tracking_process, args=(CAMERAS_INDEX,))
    send_to_processing_thread = threading.Thread(target=data_send_process)
    send_to_unity_thread = threading.Thread(target=monitor_folder, args=(FOLDER_PATH, SERVER_HOST, SERVER_PORT))

    tracking_thread.start()
    send_to_processing_thread.start()
    send_to_unity_thread.start()

    tracking_thread.join()
    send_to_processing_thread.join()
    send_to_unity_thread.join()
