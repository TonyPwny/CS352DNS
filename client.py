
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
        rootServerPort = #user input#
        # Define the port on which you want to connect to the server
        rootdns_addr = socket.gethostbyname(socket.gethostname())
        rootDNS_binding = (rootdns_addr, rootServerPort)
        rootSocket.connect(rootDNS_binding)


        except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    try:
        TopLevelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Top Level DNS socket created")
        # Define the port on which you want to connect to the server
        TopLevelport = #user input- rs listening port#
        topLevel_addr = socket.gethostbyname(socket.gethostname())
        topLevelServer_binding = (toplevel_addr, TopLevelport)
        TopLevelSocket.connect(topLevelserver_binding)


        except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()



    ## Receive data from the server
    #data_from_server=cs.recv(100)
    #print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # close the client socket
#    cs.close()
#    exit()
