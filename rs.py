# A simplified root dns server
# Nicolas Gundersen neg62
# Anthony Tiongson ast119
import threading
import time
import random
import socket
import sys

def server():


    port = int(sys.argv[1])

# This reads the PROJI - DNSRS.txt file
    rootDNSFile = open("PROJI-DNSRS.txt", 'r')
# Create an empty Dictionary
    rootDNSDict = {}
# for each line in rootDNSFile, split that line and have that line take the shape
# of (key, ip, flag), The key holds the value of the ip and the flag.
    for line in rootDNSFile:
        (key, ip, flag) = line.split()
        rootDNSDict[key] = ip, flag

    try:
        RootSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[RS]: Root DNS socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    rootServer_Binding = ('', port)
    RootSocket.bind(rootServer_Binding)
    RootSocket.listen(1)
    host = socket.gethostname()
    print("[RS]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[RS]: Server IP address is {}".format(localhost_ip))
    csockid, addr = RootSocket.accept()
    print ("[RS]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client, Here we want to send them the string
    #we were looking for
    message = "Welcome to CS 352 RS Server!"
    csockid.send(message.encode('utf-8'))
    # FOR Loop here where we compare the addresses given in the file
    # to the addresses in Proj-I DNSRS.txt
    # Close the server socket
    RootSocket.close()
    exit()

if __name__ == "__main__":

        t1 = threading.Thread(name='server', target=server)
        t1.start()

        time.sleep(random.random() * 5)

        print("Done.")
