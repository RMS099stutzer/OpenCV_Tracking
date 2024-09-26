# client.py
import socket

# サーバーのIPアドレスとポート番号を設定
SERVER_HOST = '192.168.1.2'  # サーバーPCのIPアドレスに置き換える
SERVER_PORT = 5000           # ポート番号

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

if __name__ == "__main__":
    # 送信するファイルのパス
    send_file('data.txt')  # data.txtは送信する2次元配列のtxtファイル
