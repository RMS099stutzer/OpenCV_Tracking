import socket
import os
import time

# サーバーのIPアドレスとポート番号を設定
SERVER_HOST = '169.254.13.242'  # server側のIPアドレスに置き換える
SERVER_PORT = 5000              # ポート番号

def send_file(file_path):
    # ソケットを作成し、TCP接続を設定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f'Connected to server {SERVER_HOST}:{SERVER_PORT}')
        
        # ファイルを開いて送信
        with open(file_path, 'rb') as file:
            for data in iter(lambda: file.read(1024), b''):
                client_socket.sendall(data)
        
        print('File sent successfully.')

def monitor_folder(folder_path):
    # 最初に既存のファイルを取得
    files_set = set(os.listdir(folder_path))
    print(f'Monitoring folder: {folder_path}')

    while True:
        time.sleep(5)  # 5秒ごとにフォルダを監視
        new_files_set = set(os.listdir(folder_path))
        
        # 新しいファイルがあればそれを特定
        new_files = new_files_set - files_set
        if new_files:
            for file_name in new_files:
                file_path = os.path.join(folder_path, file_name)
                print(f'New file detected: {file_name}')
                send_file(file_path)  # 新しいファイルを送信
            
            # 現在のファイル状態を更新
            files_set = new_files_set

if __name__ == "__main__":
    monitor_folder('"C:\Users\317ri\Downloads\test_data"')  # フォルダのパスを指定
