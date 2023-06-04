import threading
import time
from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock


class Client:
    '''
    for communication with the server
    '''
    BUFSIZE = 512
    HOST = 'localhost'
    PORT = 5500
    ADDR = (HOST, PORT)

    def __init__(self, name):
        '''
        init object and send name to the server
        :param name: 
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_messages(name)
        self.lock = Lock()

    def receive_messages(self):
        '''
        receives messages from the server
        :return: None
        '''
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZE).decode()

                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()

            except Exception as e:
                print("[FAILURE]", e)
                break

    def send_messages(self, msg):
        '''
        send messaged from the client to the server
        :param msg: str
        :return: None
        '''
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()

        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        '''
        return the list of messages
        :return: list
        '''
        msgs_copy = self.messages[:]
        # make sure memory safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return msgs_copy

    def disconnect(self):
        self.send_messages("{quit}")
