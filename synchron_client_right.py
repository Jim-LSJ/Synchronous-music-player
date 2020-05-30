import pygame
import os
import socket
import time, datetime

pygame.mixer.init()
pygame.mixer.music.load(os.path.join('sound', 'right.wav'))

HOST = '192.168.168.12'
PORT = 12200

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
print('Connect to server')
while True:

    server_clock = int(server.recv(1024).decode())

    client_clock = round(datetime.datetime.now().timestamp() * 1000)

    server.send( str(client_clock).encode() )


    start_time = int(round(float(server.recv(1024).decode())))
    
    while round(datetime.datetime.now().timestamp() * 1000) < start_time:
        continue

    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
    # Start = bool(s.recv(1024).decode())
    # Break = False
    # print(Start, type(Start))
    # if Start:
        # pygame.mixer.music.load(os.path.join('sound', 'right.wav'))
        # pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy() == True:
        #     Break = bool(s.recv(1024).decode())
        #     if Break:
        #         break 
        #     continue
    
    # if Break:
        # break

server.close()