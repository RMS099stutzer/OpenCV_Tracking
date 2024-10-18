import socket
import os

# サーバーのIPアドレスとポート番号を設定
SERVER_HOST = '0.0.0.0'  # 全てのネットワークインターフェースから接続を受け付ける
SERVER_PORT = 5000       # クライアント側と同じポート番号

def receive_file():
    # ソケットを作成し、TCP接続を設定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f'Server listening on {SERVER_HOST}:{SERVER_PORT}')
        
        while True:
            conn, addr = server_socket.accept()
            print(f'Connected by {addr}')
            
            # ファイル名を受信
            file_name = conn.recv(1024).decode('utf-8')
            if not file_name:
                print("No filename received.")
                conn.close()
                continue
            
            # 新しいファイルを作成して受信
            with open(file_name, 'wb') as file:  # 'wb'モードで新規作成
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    print(f'Received {len(data)} bytes for file {file_name}.')
            
            print(f'File reception completed for {file_name}.')
            conn.close()  # クライアントとの接続を閉じる

if __name__ == "__main__":
    receive_file()  # ファイルを受信する
