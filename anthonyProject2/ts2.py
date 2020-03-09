# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# TS2 (a simplified top-level DNS server)
#
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv

import sys, threading, time, random, socket

def server():

    # Establish port via command-line argument
    port = int(sys.argv[1])
    
    # Create file object to read TS DNS table
    TSFile = open("PROJ2-DNSTS2.txt", "r")
    
    # Initialize dictionary for DNS table
    DNSTable = {}
    
    # Store TS DNS table in dictionary
    for line in TSFile:
    
        hostname, IPaddress, flag = line.split()
        hostname = hostname.lower()
        DNSTable[hostname] = hostname + " " + IPaddress + " " + flag
        
    print("Creating DNS dictionary: " + str(DNSTable) + "\n")

    try:
    
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("TS server socket created: port " + str(port) + "\n")
    except socket.error as socketError:
    
        print('TS socket already open, error: {}\n'.format(socketError))
        exit()
        
    serverBinding = ('', port)
    serverSocket.bind(serverBinding)
    serverSocket.listen(1)
    TSHostname = socket.gethostname()
    print("TS server hostname: {}".format(TSHostname))
    localhostIP = (socket.gethostbyname(TSHostname))
    print("TS server IP address: {}".format(localhostIP))
    
    while True:
    
        clientSocketID, address = serverSocket.accept()
        print("Received client connection request from: {}".format(address))
    
        # Receive hostname query from the client
        queryFromClient = clientSocketID.recv(256)
    
        # The client is done querying
        if queryFromClient == "shutdownTSServer":
        
            print("Received shutdown command...")
            clientSocketID.close()
            break
        # If hostname is in dictionary, send hostname information
        elif queryFromClient in DNSTable:
        
            clientSocketID.send(str(DNSTable[queryFromClient]).encode('utf-8'))
            # Close the client socket connection
            print("\nClosing socket connection.\n")
            clientSocketID.close()
        # Hostname not in dictionary, do not do anything
    
    # Close the server socket and shutdown server
    serverSocket.close()
    exit()

if __name__ == "__main__":

    thread = threading.Thread(name='server', target = server)
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\nTS server thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)

