import socket
import os
import time
import threading
import keyboard

# サーバーのIPアドレスとポート番号を設定
SERVER_HOST = '169.254.44.200'  # server側のIPアドレスに置き換える
SERVER_PORT = 6000              # ポート番号

is_monitoring = False  # 監視状態を示すフラグ

def send_file(file_path):
    # ソケットを作成し、TCP接続を設定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f'Connected to server {SERVER_HOST}:{SERVER_PORT}')
        
        # ファイル名をまず送信
        file_name = os.path.basename(file_path)
        client_socket.sendall(file_name.encode('utf-8'))  # ファイル名を送信
        
        # サーバーがファイル名を受け取るのを待つ
        time.sleep(1)  # 短い待機

        # ファイルを開いて送信
        with open(file_path, 'rb') as file:
            for data in iter(lambda: file.read(1024), b''):
                client_socket.sendall(data)
        
        print(f'File {file_path} sent successfully.')

def monitor_folder(folder_path):
    global is_monitoring
    # 最初に既存のファイルを取得
    files_set = set(os.listdir(folder_path))
    print(f'Monitoring folder: {folder_path}')

    while True:
        if is_monitoring:
            time.sleep(1)  # 5秒ごとにフォルダを監視
            new_files_set = set(os.listdir(folder_path))

            print(f'Files in folder: {new_files_set}')
            
            # 新しいファイルがあればそれを特定
            new_files = new_files_set - files_set
            if new_files:
                for file_name in new_files:
                    file_path = os.path.join(folder_path, file_name)
                    print(f'New file detected: {file_name}')
                    send_file(file_path)  # 新しいファイルを送信
                
                # 現在のファイル状態を更新
                files_set = new_files_set
        else:
            time.sleep(1)  # 監視が停止しているときは少し待つ

def start_monitoring():
    global is_monitoring
    is_monitoring = True
    print("Monitoring started...")

def stop_monitoring():
    global is_monitoring
    is_monitoring = False
    print("Monitoring stopped.")

if __name__ == "__main__":
    
    ###################################################################
    #フォルダのパス変更は
    #　ここ！！！！！！！！！ 
    ###################################################################
    folder_path = r"C:\Users\shirokuma89dev-win10\Documents\GitHub\OpenCV_Tracking\visualization\csv"  # 監視するフォルダのパスを記入
    
    # 監視を別スレッドで開始
    monitoring_thread = threading.Thread(target=monitor_folder, args=(folder_path,))
    monitoring_thread.start()

    # キー入力の監視
    keyboard.add_hotkey('s', start_monitoring)  # 's'キーで監視開始

    # メインスレッドは待機
    keyboard.wait('esc')  # 'esc'キーでプログラムを終了
    print("Program terminated.")
