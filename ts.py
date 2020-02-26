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
    # This reads the PROJI - DNSTS.txt file
    TSFiles = open("PROJI-DNSTS.txt", 'r')
    # Create an empty Dictionary
    topLevelDict = {}
    # for each line in rootDNSFile, split that line and have that line take the shape
    # of (key, ip, flag), The key holds the value of the ip and the flag.
    for line in TSFiles:
        (key, ip, flag) = line.split()
        topLevelDict[key] = ip, flag



    try:
        topLevelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS]: Top Level socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    topLevelServer_binding = ('', port)
    topLevelSocket.bind(topLevelServer_binding)
    topLevelSocket.listen(1)
    host = socket.gethostname()
    print("[TS]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS]: Server IP address is {}".format(localhost_ip))
    csockid, addr = topLevelSocket.accept()
    print ("[TS]: Got a connection request from a client at {}".format(addr))


    topLevelSocket.close()
    exit()

if __name__ == "__main__":
        t1 = threading.Thread(name='server', target=server)
        t1.start()

        time.sleep(random.random() * 5)

        print("Done.")


    # Close the server socket
