import pygame
import os
import socket
import time, datetime

pygame.mixer.init()

client_manager = []

HOST, PORT = socket.gethostname(), 12200
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind((HOST, PORT))
print('HOST: {}, PORT: {}'.format(socket.gethostbyname(socket.gethostname()), PORT))
while True:
    s.listen(5)

    print('The server is running')
    # max_time = 0

    if len(client_manager) != 2:
        try:
            client, address = s.accept()
            print('Connect to {}'.format(address))

            server_clock = round(datetime.datetime.now().timestamp() * 1000)

            client.send( str(server_clock).encode() )

            client_clock = int(client.recv(1024).decode())

            round_trip_time = round(datetime.datetime.now().timestamp() * 1000) - server_clock
            client_true_clock = client_clock - round_trip_time / 2

            clock_gap = client_true_clock - server_clock

            client_manager.append((client, clock_gap, round_trip_time))
            # max_time = round_trip_time if round_trip_time > max_time else max_time
        except KeyboardInterrupt:
            client.send(str(True).encode())
            client.close()
            break

    else:
        start = input("Enter any key to start")
        timestamp_now = datetime.datetime.now().timestamp() * 1000
        offset = 500
        for cli in client_manager:
            # toc = time.clock()
            # loop_delay = toc - tic
            cli[0].send( str(timestamp_now + cli[1] + offset).encode() )

        try:
            while True:
                pass
        except KeyboardInterrupt:
            for cli in client_manager:
                cli[0].close()
            break

s.close()