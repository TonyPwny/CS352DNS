
# Nicolas Gundersen neg62
# Anthony Tiongson ast119
import threading
import time
import random
import socket

def client():
    #This populates a list with the addresses in the PROJI-HNS.txt
    file = open("PROJI-HNS.txt", 'r')




    try:
        RootSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Root DNS socket created")
        RootServerPort = #user input#
        # Define the port on which you want to connect to the server
        rootdns_addr = socket.gethostbyname(socket.gethostname())
        server_binding = (rootdns_addr, rsport)
        RootSocket.connect(server_binding)

        except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()



#I was thinking of having 2 tries? Both transmitting strings across sockets to said dns server
    try:
        TopLevelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Top Level DNS socket created")
        # Define the port on which you want to connect to the server
        TopLevelport = #user input- rs listening port#
        toplevel_addr = socket.gethostbyname(socket.gethostname())
        server_binding = (toplevel_addr, tsport)
        TopLevelSocket.connect(server_binding)



        except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()



    # Receive data from the server
    data_from_server=cs.recv(100)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # close the client socket
    cs.close()
    exit()
