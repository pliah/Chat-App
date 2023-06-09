from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


from person import Person

BUFSIZE = 512
HOST = 'localhost'
PORT = 5500
ADDR = (HOST,PORT)
MAX_CONN = 10

persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) #set up server

def broadcast(msg, name):
    '''
    send the new message to all the clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    '''
    for person in persons:
        client = person.client
        client.send(bytes(name, "utf8") + msg)

def client_communication(person):
    '''
    thread to handle all the message received from the client
    :param person: Person
    :return: None
    '''
    run = True
    client = person.client
    # get persons name
    name = client.recv(BUFSIZE).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} had joined the chat!", "utf8")
    broadcast(msg, "") #braodcast welcome message

    while run:
        try:
            msg = client.recv(BUFSIZE)
            if msg == bytes("{quit}", "utf8"):
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has just left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name + ": ")
                print(f"{name}:  ", msg.decode("utf8"))
        except Exception as e:
            print(f"[1FAILURE] {person.name}", e)
            run = False

def wait_for_connection():
    '''
    waite for connection from the clients, and start a new thread once connected
    :param SERVER:
    :return: None
    '''
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)

            print(f"CONNECTION {addr} connected to the server at {datetime.now()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE]", e)
            run = False
    print("Server crashed")


if __name__ == "__main__":
    SERVER.listen(MAX_CONN)
    print("[START] Waiting fot connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
