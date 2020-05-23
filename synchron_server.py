import pygame
import os
import socket
import time
HOST = '127.0.0.1'
PORT = 12200

HOST, PORT = '127.0.0.1', 12200
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind ( ( HOST , PORT ) )

while True:
    s.listen(5)

    print('The server is running')
    
    try:
        while True:
            client, address = s.accept()
            print('Connect to {}'.format(address))

            # start
            Start = True
            client.send(str(Start).encode())

            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join('sound', 'left.wav'))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            
    except KeyboardInterrupt:
        client.send(str(True).encode())
        client.close()
        break
s.close()