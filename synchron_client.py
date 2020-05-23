import pygame
import os
import socket
import time
HOST = '127.0.0.1'
PORT = 12200

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    Start = bool(s.recv(1024).decode())
    Break = False
    print(Start, type(Start))
    if Start:
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join('sound', 'right.wav'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            Break = bool(s.recv(1024).decode())
            if Break:
                break 
            continue
    
    if Break:
        break

s.close()