import socket, threading

port = 5000
host = "10.0.0.189"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen(100)

clients = []


def start():
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        t = threading.Thread(target=send, args=(conn,))
        t.start()

def send(fromConnection):
    try:
        while True:
            data = fromConnection.recv(4096)
            for cl in clients:
                if cl != fromConnection:
                    cl.send(data)
    except:
        print("Client Disconnected")

print("SERVER STARTED")
start()