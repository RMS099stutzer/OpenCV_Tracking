import socket
import time

host = "10.101.224.180" #Processingで立ち上げたサーバのIPアドレス
port = 10001       #Processingで設定したポート番号

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成

def socket_connect():
    time.sleep(1)
    global socket_client, host, port
    socket_client.connect((host, port))

def data_transfer_coord(xyz_coord):
    time.sleep(0.05)
    if None not in xyz_coord:
        socket_client.send(("FFFF," + str(round(xyz_coord[0])) + "," + str(round(xyz_coord[1])) + "," + str(round(xyz_coord[2]))).encode('utf-8'))
        return
    
    socket_client.send(("AAAA," + str(1) + "," + str(1) + "," + str(1)).encode('utf-8'))
    return

    

# socket_client.send(("FFFF," + str(200) + "," + str(round(np.sin(20),3)*100 + 150) + "," + str(round(np.cos(20),3)*100 + 150)).encode('utf-8'))
# time.sleep(0.07)
# socket_client.send(("AAAA," + str(1) + "," + str(1) + "," + str(1)).encode('utf-8'))  #AAAAの後は適当な数字でいい
# time.sleep(0.07)
# for i in np.arange(0.0, 20.0, 0.5):
#     print("FFFF," + str(i*10) + "," + str(round(np.cos(i),3)*100 + 150) + "," + str(round(np.sin(i),3)*100 + 150))
#     socket_client.send(("FFFF," + str(round(np.cos(i),3)*100 + 150) + "," + str(round(np.sin(i),3)*100 + 150) + "," + str(i*10)).encode('utf-8'))
#     time.sleep(0.07)
# socket_client.send(("1111," + str(round(np.cos(20),3)*100 + 150) + "," + str(round(np.sin(20),3)*100 + 150) + "," + str(200)).encode('utf-8'))
# socket_client.close()