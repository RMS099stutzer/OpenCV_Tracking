import sys
import os
import threading
import socket

sys.path.append(os.path.join(os.path.dirname(__file__), "tracking"))

# tracking/main.py
from tracking.main import tracking_process, data_send_process

# socket_com/sender.py
from socket_com.sender import monitor_folder

###################### 当日設定する必要があるもの【ここから】 ######################
SERVER_HOST = "169.254.44.200"  # server側のIPアドレスに置き換える
###################### 当日設定する必要があるもの【ここまで】 ######################

CAMERAS_INDEX = [2, 1]
FOLDER_PATH = r"./visualization/csv"  # 監視するフォルダのパスを記入
SERVER_PORT = 6000  # ポート番号

MY_PORT = 10001

import socket

def clear_folder(folder_path):
    """指定されたフォルダ内のすべてのファイルを削除する"""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def get_ip_address():
    hostname = socket.gethostname()  # ホスト名を取得
    ip_address = socket.gethostbyname(hostname)  # ホスト名からIPアドレスを取得
    return ip_address


if __name__ == "__main__":
    clear_folder(FOLDER_PATH)

    MY_IP = get_ip_address()
    print(f"Your IP Address: {MY_IP}")

    tracking_thread = threading.Thread(target=tracking_process, args=(CAMERAS_INDEX,))
    send_to_processing_thread = threading.Thread(
        target=data_send_process, args=(MY_IP, MY_PORT)
    )
    send_to_unity_thread = threading.Thread(
        target=monitor_folder, args=(FOLDER_PATH, SERVER_HOST, SERVER_PORT)
    )

    tracking_thread.start()
    send_to_processing_thread.start()
    send_to_unity_thread.start()

    tracking_thread.join()
    send_to_processing_thread.join()
    send_to_unity_thread.join()
