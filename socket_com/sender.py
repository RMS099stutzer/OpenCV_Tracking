import socket
import os
import time


def send_file(file_path, server_host, server_port):
    # ソケットを作成し、TCP接続を設定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(5)  # タイムアウトを設定
        try:
            client_socket.connect((server_host, server_port))
        except Exception as e:
            print(f"An error occurred: {e}")
            return

        print(f"Connected to server {server_host}:{server_port}")

        # ファイル名をまず送信
        file_name = os.path.basename(file_path)
        client_socket.sendall(file_name.encode("utf-8"))  # ファイル名を送信

        # サーバーがファイル名を受け取るのを待つ
        time.sleep(1)  # 短い待機

        # ファイルを開いて送信
        with open(file_path, "rb") as file:
            for data in iter(lambda: file.read(1024), b""):
                client_socket.sendall(data)

        print(f"File {file_path} sent successfully.")


def monitor_folder(folder_path, server_host, server_port):
    # 最初に既存のファイルを取得
    files_set = set(os.listdir(folder_path))
    print(f"Monitoring folder: {folder_path}")

    while True:
        new_files_set = set(os.listdir(folder_path))

        print(f"Files in folder: {new_files_set}")

        # 新しいファイルがあればそれを特定
        new_files = new_files_set - files_set
        if new_files:
            for file_name in new_files:
                file_path = os.path.join(folder_path, file_name)
                print(f"New file detected: {file_name}")
                send_file(file_path, server_host, server_port)  # 新しいファイルを送信

            # 現在のファイル状態を更新
            files_set = new_files_set

        time.sleep(1)  # 監視が停止しているときは少し待つ


if __name__ == "__main__":
    ###################################################################
    # フォルダのパス変更は
    # 　ここ！！！！！！！！！
    # Note 10/23/2023: これはsender.pyを直接呼び出す時のやつです。
    # 普段はルートディレクトリのconfig.pyを設定してください。
    ###################################################################
    folder_path = r"./visualization/csv"  # 監視するフォルダのパスを記入
    SERVER_HOST = "169.254.44.200"  # server側のIPアドレスに置き換える
    SERVER_PORT = 6000  # ポート番号

    monitor_folder(folder_path, server_host=SERVER_HOST, server_port=SERVER_PORT)
