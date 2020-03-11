# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# TS1 (a simplified top-level DNS server)
#
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv

import random, socket, sys, threading, time

# makeDNSTable function stores a DNS table from a file into a dictionary
def makeDNSTable(file, dictionary):

    for line in file:

        hostname, IPaddress, flag = line.split()
        hostname = hostname.lower()
        dictionary[hostname] = hostname + " " + IPaddress + " " + flag
        
    file.close()
    print("Created DNS dictionary: " + str(dictionary) + "\n")

# socketOpen function to open and return a socket in a given port designated by a label.
def socketOpen(label, port):

    try:
    
        socketOpen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketOpenPrompt = "Socket opened to connect to " + label + ": port " + str(port) + "\n"
        print(socketOpenPrompt)
        return socketOpen
    except socket.error as socketOpenError:
    
        socketOpenError = label + ' socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        exit()

# Print out the hostname and IP address for a server designated by a label
def serverInfo(label):
    
    hostname = socket.gethostname()
    print(label + " hostname: {}".format(hostname))
    localhostIP = (socket.gethostbyname(hostname))
    print(label + " IP address: {}".format(localhostIP))

# evaluate function accepts a given clientSocket connection designated by a given label and receives data to check against a given dictionary
def evaluate(label, clientSocket, dictionary):

    while True:
    
        clientConnection, address = clientSocket.accept()
        print("Received " + label + " connection request from: {}".format(address))
    
        # Receive hostname query from the client
        queryFromClient = clientConnection.recv(256)
    
        # The client is done querying
        if queryFromClient == "shutdownTSServer":
        
            print("\nReceived shutdown command...\n")
            clientConnection.close()
            break
        # If hostname is in dictionary, send hostname information
        elif queryFromClient in dictionary:
        
            clientConnection.send(str(dictionary[queryFromClient]).encode('utf-8'))
            # Close the client socket connection
            print("\nClosing " + label + " socket connection.\n")
            clientConnection.close()
        # Hostname not in dictionary, do not do anything

def server(label, clientLabel, file):

    # Establish port via command-line argument
    port = int(sys.argv[1])
    
    # Initialize dictionary for DNS table
    DNSTable = {}
    
    # Store TS DNS table in file in the dictionary DNSTable
    makeDNSTable(file, DNSTable)

    # Open client socket and listen
    client = socketOpen(clientLabel, port)
    client.bind(('', port))
    client.listen(1)
    
    # Print out TS1's hostname and its respective IP address
    serverInfo(label)
    
    # Accept a client socket connection and receives data to check against the DNSTable.
    evaluate(clientLabel, client, DNSTable)
    
    # Close the client socket and shutdown server
    client.close()
    exit()

if __name__ == "__main__":

    label = "TS1Server"
    clientLabel = "TS1Client"
    
    # Create file object to read TS DNS table
    file = open("PROJ2-DNSTS1.txt", "r")
    
    thread = threading.Thread(name='server', target = server, args = (label, clientLabel, file,))
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\n" + label + " thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)
