import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# global constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
BUFSIZE = 512

# global variable
messages = []
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)



def receive_messages():
    '''
    receives messages from the server
    :return: None
    '''
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode("utf8")
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[FAILURE]", e)


def send_messages(msg):
    '''
    send messaged from the client to the server
    :param msg: str
    :return: None
    '''
    global client_socket
    try:
        client_socket.send(bytes(msg, "utf8"))
        if msg == bytes("{quit}", "utf8"):
            client_socket.close()
    except Exception as e:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)
        print("[FAILURE]",e)





receive_thread = Thread(target=receive_messages)
receive_thread.start()

send_messages("Pliah")
send_messages("hello")
time.sleep(10)
send_messages("{quit}")


