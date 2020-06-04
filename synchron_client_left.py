import pygame
import os
import socket
import time, datetime


def counter():
    count = 1
    add = False
    while True:
        if (round(time.time() * 10) % 10 == 9 and not add):
            print('\r{:5d}'.format(count), end='')
            count += 1
            add = True
        if (round(time.time() * 10) % 10 != 9):
            add = False


pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096 * 16)
pygame.mixer.music.load(os.path.join('sound', 'left.mp3'))

HOST = '172.20.10.2'
PORT = 12200

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
print('Connect to server')
while True:

    server_clock = int(server.recv(1024).decode())

    client_clock = round(time.time() * 1000)

    server.send( str(client_clock).encode() )


    start_time = int(round(float(server.recv(1024).decode())))
    print(start_time)

    while round(time.time() * 1000) < start_time:
        continue
    pygame.mixer.music.play(loops=0, start=0.0)

    # counter()
    server.settimeout(1)
    flag = 0
    while pygame.mixer.music.get_busy() == True:
        try:
            flag = server.recv(1024).decode().split(',')
            if flag[0] == 'stop':
                flag = 1
                break
            elif flag[0] == 'pause':
                pause_time = flag[1]
                print(pause_time)

                while round(time.time() * 1000) < pause_time:
                    continue
                pygame.mixer.music.pause()
            elif flag[0] == 'play':
                unpause_time = flag[1]
                print(unpause_time)

                while round(time.time() * 1000) < unpause_time:
                    continue
                pygame.mixer.music.unpause()
        except socket.timeout:
            pass
        continue
    if flag:
        break
    

server.close()