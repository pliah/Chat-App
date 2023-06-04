from client import Client
import time
from threading import Thread

client1 = Client("Pliah")
client2 = Client("Jackov")
client3 = Client("Shira")

def update_messages():
    '''
    updates the local list of messages
    :return: None
    '''
    msgs = []
    run = True
    while run:
        time.sleep(0.1)
        new_messages = client1.get_messages()
        msgs.extend(new_messages)
        for msg in new_messages:
            print(msg)
            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()
client1.send_messages("hello")
time.sleep(1)
client2.send_messages("Hi")
time.sleep(1)
client3.send_messages("Hiiiiiiiiiiiiiiiiiiiiiiiii")
time.sleep(1)
client1.send_messages("How are you?")
time.sleep(1)
client2.send_messages("Fine")
time.sleep(1)
client1.send_messages("O.K.")
time.sleep(5)
client1.disconnect()
time.sleep(5)
client2.disconnect()

