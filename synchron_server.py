import pygame
import os
import socket
import time, datetime

pygame.mixer.init()

client_manager = []

HOST, PORT = '172.20.10.2', 12200
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind((HOST, PORT))
print('HOST: {}, PORT: {}'.format(socket.gethostbyname(socket.gethostname()), PORT))
while True:
    s.listen(5)

    print('The server is running')
    max_time = 0

    if len(client_manager) != 2:
        try:
            client, address = s.accept()
            print('Connect to {}'.format(address))

            server_clock = round(time.time() * 1000)

            client.send( str(server_clock).encode() )

            client_clock = int(client.recv(1024).decode())

            round_trip_time = round(time.time() * 1000) - server_clock
            client_true_clock = client_clock - round_trip_time / 2

            clock_gap = client_true_clock - server_clock

            client_manager.append((client, clock_gap, round_trip_time))
            
            max_time = round_trip_time if round_trip_time > max_time else max_time
        
        except KeyboardInterrupt:
            client.send(str(True).encode())
            client.close()
            break

    else:
        start = input("Enter any key to start")
        start_time = time.time() * 1000
        offset = max_time / 2 + 100
        for cli in client_manager:
            cli[0].send( str(start_time + cli[1] + offset).encode() )

        play_time = 0
        play_flag = True
        try:
            while True:
                control = input("Control")
                if control == "+":
                    for cli in client_manager:
                        cli[0].send('+'.encode())
                    continue
                elif control == "-":
                    for cli in client_manager:
                        cli[0].send('-'.encode())
                    continue
                elif control == "l+":
                    client_manager[0][0].send('+'.encode())
                    continue
                elif control == "l-":
                    client_manager[0][0].send('-'.encode())
                    continue
                elif control == "r+":
                    client_manager[1][0].send('+'.encode())
                    continue
                elif control == "r-":
                    client_manager[1][0].send('-'.encode())
                    continue
                elif control == "next":
                    continue
                if play_flag:
                    max_time = 0
                    for cli in client_manager:
                        server_clock = round(time.time() * 1000)
                        cli[0].send( ('pause,' + str(server_clock)).encode())
                        client_clock = int(cli[0].recv(1024).decode())
                        rtt = round(time.time() * 1000) - server_clock
                        max_time = rtt if rtt > max_time else max_time
                    timestamp_now = time.time() * 1000
                    play_time = play_time + timestamp_now - start_time
                    offset = max_time / 2 + 100
                    for cli in client_manager:
                        cli[0].send( str(timestamp_now + cli[1] + offset).encode())
                    play_flag = False
                else:
                    max_time = 0
                    for cli in client_manager:
                        server_clock = round(time.time() * 1000)
                        cli[0].send( ('play,' + str(server_clock)).encode())
                        client_clock = int(cli[0].recv(1024).decode())
                        rtt = round(time.time() * 1000) - server_clock
                        max_time = rtt if rtt > max_time else max_time
                    timestamp_now = time.time() * 1000
                    start_time = timestamp_now
                    offset = max_time / 2 + 100
                    for cli in client_manager:
                        cli[0].send((str(timestamp_now + cli[1] + offset) + ',' + str(play_time)).encode())
                    play_flag = True

        except KeyboardInterrupt:
            for cli in client_manager:
                cli[0].send(str('stop').encode())
                cli[0].close()
                s.close()
            break

s.close()