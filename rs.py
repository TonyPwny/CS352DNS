# A simplified root dns server
# Nicolas Gundersen neg62
# Anthony Tiongson ast119
import threading
import time
import random
import socket

def server():
    file = open("PROJI-DNSRS.txt", 'r')



    try:
        RootSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Root DNS socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()


    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client, Here we want to send them the string
    #we were looking for

    # FOR Loop here where we compare the addresses given in the file
    # to the addresses in Proj-I DNSRS.txt

    msg = "Welcome to CS 352!"
    csockid.send(msg.encode('utf-8'))

    # Close the server socket
    ss.close()
    exit()
