# server.py
import socket

# サーバーのIPアドレスとポート番号を設定
HOST = '0.0.0.0'  # 任意のIPアドレスからの接続を許可
PORT = 5000        # ポート番号

def start_server():
    # ソケットを作成し、TCP接続を設定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f'Server listening on {HOST}:{PORT}')

        # クライアントからの接続を待機
        conn, addr = server_socket.accept()
        with conn:
            print(f'Connected by {addr}')
            # ファイルデータを受信
            with open('received_data.txt', 'wb') as file:
                while True:
                    data = conn.recv(1024)  # 1024バイトずつ受信
                    if not data:
                        break
                    file.write(data)
            print('File received successfully.')

if __name__ == "__main__":
    start_server()
