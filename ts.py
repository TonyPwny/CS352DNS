# A simplified root dns server
# Nicolas Gundersen neg62
# Anthony Tiongson ast119
import threading
import time
import random
import socket

def server():
    file = open("PROJI-DNSTS.txt", 'r')





    try:
        topLevelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS]: Top Level socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    topLevelServer_binding = ('', 50007)
    topLevelServer.bind(topLevelServer_binding)
    topLevelServer.listen(1)
    host = socket.gethostname()
    print("[TS]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS]: Server IP address is {}".format(localhost_ip))
    csockid, addr = topLevelSocket.accept()
    print ("[TS]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.
    

    # Close the server socket
    topLevelSocket.close()
    exit()
