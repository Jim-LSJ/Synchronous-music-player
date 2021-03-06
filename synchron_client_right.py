import pygame
import os
import socket
import time, datetime


# def counter():
#     count = 1
#     add = False
#     while True:
#         if (round(time.time() * 10) % 10 == 9 and not add):
#             print('\r{:5d}'.format(count), end='')
#             count += 1
#             add = True
#         if (round(time.time() * 10) % 10 != 9):
#             add = False


pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096 * 16)
idx=0
music_list = os.listdir('sound_right')
list_len = len(music_list)

HOST = '172.20.10.2'
PORT = 12200

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
print('Connect to server')
server_clock = int(server.recv(1024).decode())

client_clock = round(time.time() * 1000)

server.send( str(client_clock).encode() )
while True:
    pygame.mixer.music.load(os.path.join('sound_right',music_list[idx]))

    start_time = int(round(float(server.recv(1024).decode())))
    print(start_time)

    while round(time.time() * 1000) < start_time:
        continue
    pygame.mixer.music.play(loops=0, start=0.0)

    # counter()
    server.settimeout(1)
    stop_flag = 1
    while pygame.mixer.music.get_busy() == True:
        try:
            flag = server.recv(1024).decode().split(',')
            if flag[0] == 'stop':
                break
            elif flag[0] == 'pause':
                server_clock = int(round(float(flag[1])))
                client_clock = round(time.time() * 1000)
                server.send( str(client_clock).encode() )

                pause_time = int(round(float(server.recv(1024).decode())))
                print(pause_time)

                while round(time.time() * 1000) < pause_time:
                    continue
                pygame.mixer.music.pause()
            elif flag[0] == 'play':
                server_clock = int(round(float(flag[1])))
                client_clock = round(time.time() * 1000)
                server.send( str(client_clock).encode() )

                play_param = server.recv(1024).decode().split(',')
                unpause_time = int(round(float(play_param[0])))
                
                music_pos = pygame.mixer.music.get_pos()
                unpause_pos = int(round(float(play_param[1])))
                unapuse_time = unpause_time + music_pos - unpause_pos

                print(unpause_time)

                while round(time.time() * 1000) < unpause_time:
                    continue
                pygame.mixer.music.unpause()# play(loops=0, start=float(play_param[1]) / 1000)

            elif flag[0] == '+':
                volume = pygame.mixer.music.get_volume() + 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)# default = 1.0, range = 0.0~1.0
            elif flag[0] == '-':
                volume = pygame.mixer.music.get_volume() - 0.1
                if volume < 0:
                    volume = 0
                pygame.mixer.music.set_volume(volume)# default = 1.0, range = 0.0~1.0
            elif flag[0] == 'next':
                idx+=1
                if idx >= list_len:
                    idx = 0
                stop_flag = 0
                break
        except socket.timeout:
            pass
        continue
    print("music_stop")
    pygame.mixer.music.stop()
    if stop_flag:
        print("program stop")
        break
    

server.close()