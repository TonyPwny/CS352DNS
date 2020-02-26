
# Nicolas Gundersen neg62
# Anthony Tiongson ast119
import threading
import time
import random
import socket

def client():
    #This populates a list with the addresses in the PROJI-HNS.txt
    file = open("PROJI-HNS.txt", 'r'
    myURLlist = []
    for line in file:
        myURLlist.append(line.strip())
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Root DNS socket created")
        port = #user input#
        localhost_addr = socket.gethostbyname(socket.gethostname())




        except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
#I was thinking of having 2 tries? Both transmitting strings across sockets to said dns server
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Top Level DNS socket created")
        port = #user input- rs listening port#




        except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()


    # Define the port on which you want to connect to the server
        port = 6007
        localhost_addr = socket.gethostbyname(socket.gethostname())

    #connect to the server on the rs

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Receive data from the server
    data_from_server=cs.recv(100)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # close the client socket
    cs.close()
    exit()
