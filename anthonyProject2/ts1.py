# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# TS1 (a simplified top-level DNS server)
#    There are two TS servers which each maintain a DNS table consisting of
#    three fields:
#
#    - Hostname
#    - IP address
#    - Flag (A only; no NS)
#
#    For each query received from the LS, each TS server does a lookup in its
#    DNS table, and if there is a match, sends the DNS entry as a string:
#
#    Hostname IPaddress A
#
#    If the Hostname isn't found in the DNS table, the TS server sends
#    nothing back. A TS server without the hostname in its local DNS table
#    MUST NOT send any data to the LS or the client.
#
#    DNS tables can be read from PROJ2-DNSTS1.txt and PROJ2-DNSTS2.txt
#    respectively for TS1 and TS2. We will ensure that the two DNS tables
#    have no overlapping hostnames.
#
#    Note that DNS lookups are case-insensitive. If there is a hit in the
#    local DNS table, the TS programs must respond with the version of the
#    string that is in their local DNS table.
#
#    Each TS maintains just one connection -- with the LS.
#
#    python ts1.py ts1ListenPort
#    - ts1ListenPort and ts2ListenPort are ports accepting incoming connections
#    at TS1 and TS2 (resp.) from LS
#
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv

import sys, threading, time, random, socket

def server():

    # Establish port via command-line argument
    port = int(sys.argv[1])
    
    # Create file object to read TS DNS table
    TSFile = open("PROJ2-DNSTS1.txt", "r")
    
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
        # Hostname not in dictionary, just close the connection
        else:
            
            time.sleep(2.50)
            
        # Close the client socket connection
        print("\nClosing socket connection.\n")
        clientSocketID.close()
    
    # Close the server socket and shutdown server
    serverSocket.close()
    exit()

if __name__ == "__main__":

    thread = threading.Thread(name='server', target = server)
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\nTS server thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)

