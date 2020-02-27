# Anthony Tiongson
# TS (a simplified top-level DNS server)
# Try to use a dictionary to store data in PROJI-DNSTS.txt
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv

import sys, threading, time, random, socket

def server():

    # Establish port via command-line argument
    port = int(sys.argv[1])
    
    # Create file object to read TS DNS table
    TSFile = open("PROJI-DNSTS.txt", "r")
    
    # Initialize dictionary for DNS table
    DNSTable = {}
    
    # Store TS DNS table in dictionary
    for line in TSFile:
    
        hostname, IPaddress, flag = line.split()
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
    clientSocketID, address = serverSocket.accept()
    print("Received client connection request from: {}".format(address))
    
    # Server greeting message to client
    greeting = "Welcome to CS 352 TS server! Socket to me!"
    clientSocketID.send(greeting.encode('utf-8'))
    
    while True:
    
        # Receive hostname query from the client
        queryFromClient = clientSocketID.recv(64)
    
        # The client is done querying
        if queryFromClient == "EndOfQuery":
        
            break
        # If hostname is in dictionary, send hostname information
        elif queryFromClient in DNSTable:
        
            clientSocketID.send(str(DNSTable[queryFromClient]).encode('utf-8'))
        # Hostname not in dictionary, send error message
        else:
        
            clientSocketID.send(queryFromClient + " - Error:HOST NOT FOUND".encode('utf-8'))
    
    # Close the server socket
    serverSocket.close()
    exit()

if __name__ == "__main__":

    thread = threading.Thread(name='server', target = server)
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\nTS server thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)

