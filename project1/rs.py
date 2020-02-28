# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# RS (a simplified root DNS server)
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv

import sys, threading, time, random, socket

def server():
    
    # Establish port via command-line argument
    port = int(sys.argv[1])
    
    # Create file object to read RS DNS table
    RSFile = open("PROJI-DNSRS.txt", "r")
    
    # Initialize dictionary for DNS table
    DNSTable = {}
    
    # Store RS DNS table in dictionary
    for line in RSFile:
    
        hostname, IPAddress, flag = line.split()
        hostname = hostname.lower()
        DNSTable[hostname] = hostname + " " + IPAddress + " " + flag
        if flag == "NS":
            TSHostname = hostname + " - " + flag
        
    print("Creating DNS dictionary: " + str(DNSTable) + "\n")

    try:
    
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("RS server socket created: port " + str(port) + "\n")
    except socket.error as socketError:
    
        print('RS socket already open, error: {}\n'.format(socketError))
        exit()
        
    serverBinding = ('', port)
    serverSocket.bind(serverBinding)
    serverSocket.listen(1)
    RSHostname = socket.gethostname()
    print("RS server hostname: {}".format(RSHostname))
    localhostIP = (socket.gethostbyname(RSHostname))
    print("RS server IP address: {}".format(localhostIP))
    clientSocketID, address = serverSocket.accept()
    print("Received client connection request from: {}".format(address))
    
    # Server greeting message to client
    greeting = "Welcome to CS 352 RS server! Socket to me!"
    clientSocketID.send(greeting.encode('utf-8'))
    
    while True:
    
        # Receive hostname query from the client
        queryFromClient = clientSocketID.recv(256)
    
        # The client is done querying
        if queryFromClient == "EndOfQuery":
        
            break
        # If hostname is in dictionary, send hostname information
        elif queryFromClient in DNSTable:
        
            clientSocketID.send(str(DNSTable[queryFromClient]).encode('utf-8'))
        # Hostname not in dictionary, send TS server information
        else:
            
            clientSocketID.send(TSHostname.encode('utf-8'))
    
    # Close the server socket
    serverSocket.close()
    exit()

if __name__ == "__main__":

    thread = threading.Thread(name='server', target = server)
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\nRS server thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)

