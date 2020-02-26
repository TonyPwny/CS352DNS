
# Nicolas Gundersen neg62
# Anthony Tiongson ast119
import threading
import time
import random
import socket
import sys

def client():

    RSport = int(sys.argv[1])
    TSport = int(sys.argv[2])
    #This populates hostNameList with the addresses in the PROJI-HNS.txt
    hostNameFile = open("PROJI-HNS.txt", 'r')
    hostNameList = []
    for line in hostNameFile:
        hostNameList.append(line.strip())

    try:
        RootSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Root DNS socket created")
        # Define the port on which you want to connect to the server
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    try:
        TopLevelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Top Level DNS socket created")
        # Define the port on which you want to connect to the server
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    #define the port on which you want to connect to the DNS server
    localhostAddress = socket.gethostbyname(socket.gethostname())
    rootDNS_binding = (localhostAddress, RSport)
    RootSocket.connect(rootDNS_binding)

    #Receive data from the server
    dataFromDNS = RootSocket.recv(100)
    print("[C]: Data received from server: {}".format(dataFromDNS.decode('utf-8')))


    #define the port for the top level server and connect
    TopLevel_binding = (localhostAddress, TSport)
    TopLevelSocket.connect(TopLevel_binding)

    #Receive data from the server
    dataFromTS = TopLevelSocket.recv(100)
    print("[C]: Data received from server: {}".format(dataFromTS.decode('utf-8')))

     #close the client socket
    RootSocket.close()
    TopLevelSocket.close()
    exit()

if __name__ == "__main__":

    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)


    print("Done.")
