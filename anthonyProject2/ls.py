# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# LS (a simplified load-balancing DNS server)
#
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv
#   https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
#   https://stackoverflow.com/questions/13941562/why-can-i-not-catch-a-queue-empty-exception-from-a-multiprocessing-queue/13941865

import queue, random, socket, sys, threading, time

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

# socketBind function to establish and return a socket binding using a given hostname and port and designated by a label.
def socketBind(label, hostname, port):

    # Define the IP address on which you want to connect to the LS server.
    IPAddress = socket.gethostbyname(hostname)
    print("Hostname on which to connect to " + label + " server: " + hostname + "\n" + "IP address: " + str(IPAddress) + "\n")
    socketBind = (IPAddress, port)
    return socketBind

# serverInfo function prints out the hostname and IP address for a server designated by a label
def serverInfo(label):
    
    hostname = socket.gethostname()
    print(label + " hostname: {}".format(hostname))
    localhostIP = (socket.gethostbyname(hostname))
    print(label + " IP address: {}".format(localhostIP))
    
# query function to query a hostname to a server on serverSocket and to put results in a defined queue.
def query(serverSocket, hostname, queue):
    
    serverSocket.settimeout(5)
    serverSocket.send(hostname.encode('utf-8'))
    try:
    
        responseFromServer = serverSocket.recv(256).decode('utf-8')
        queue.put(responseFromServer)
    except socket.timeout, queryTimeout:

        responseFromServer = str(queryTimeout)
        queue.put(responseFromServer)
    except socket.error, queryError:
    
        # Something else happened, handle error, exit, etc.
        print queryError
        sys.exit(1)

# shutdownServer function sends a shutdown command to a server with a given hostname and port designated by a label.
def shutdownServer(label, hostname, port):

    # Tell the server to shut down and close connection.
    # Open server socket.
    server = socketOpen(label, port)
        
    # Create server socketBind and connect to the server.
    server.connect(socketBind(label, hostname, port))
    
    # Send shutdown command.
    print("Shutting down " + label + "...\n")
    shutdownCommand = "shutdown" + label
    server.send(shutdownCommand.encode('utf-8'))
    # Close connection to server socket.
    print("Closing " + label + " socket connection.\n")
    server.close()

# resolve function sends a given response to a given clientConnection and closes the current given server connections.
def resolve(clientConnection, response, serverLabelTS1, serverLabelTS2, TS1Server, TS2Server):

    clientConnection.send(response.encode('utf-8'))
    print("Closing " + serverLabelTS1 + " and " + serverLabelTS2 + " socket connections.\n")
    TS1Server.close()
    TS2Server.close()

# evaluate function tries to resolve the results from the given servers and their respective given results queues.
def evaluate(serverLabelTS1, serverLabelTS2, clientConnection, hostname, TS1Server, TS2Server, queueThreadTS1, queueThreadTS2):

    responseFromTS1Server = None
    responseFromTS2Server = None

    while True:
        
        try:
        
            responseFromTS1Server = queueThreadTS1.get_nowait()
        except queue.Empty:
            
            pass
            
        try:
        
            responseFromTS2Server = queueThreadTS2.get_nowait()
        except queue.Empty:
        
            pass
            
        if responseFromTS1Server is not None and responseFromTS1Server != "timed out":
            
            response = responseFromTS1Server
            responsePrompt = "Response received from the " + serverLabelTS1 + ": {}\n".format(response)
            break
        elif responseFromTS2Server is not None and responseFromTS2Server != "timed out":
        
            response = responseFromTS2Server
            responsePrompt = "Response received from the " + serverLabelTS2 + ": {}\n".format(response)
            break
        elif responseFromTS1Server == "timed out" and responseFromTS2Server == "timed out":
        
            response = hostname + " - Error:HOST NOT FOUND"
            responsePrompt = serverLabelTS1 + " and " + serverLabelTS2 + " timed out; could not resolve hostname..."
            break
        
    print(responsePrompt)
    resolve(clientConnection, response, serverLabelTS1, serverLabelTS2, TS1Server, TS2Server)

# queryMultiThread function takes in the servers label, a client designated by a clientLabel, and the labels, hostnames, and ports for other servers to simulataneously query hostnames from the client to the other servers
def queryMultiThread(label, clientLabel, client, serverLabelTS1, hostnameTS1, portTS1, serverLabelTS2, hostnameTS2, portTS2):

    while True:
    
        clientConnection, address = client.accept()
        print("Received " + clientLabel + " connection request from: {}".format(address))
    
        # Receive hostname query from the client
        hostname = clientConnection.recv(256)
    
        # The client is done querying
        if hostname == "shutdown" + label:
        
            print("Received shutdown command...")
            
            # Tell the TS1 and TS2 servers to shut down and close connections
            shutdownServer(serverLabelTS1, hostnameTS1, portTS1)
            shutdownServer(serverLabelTS2, hostnameTS2, portTS2)
            break
        # Send hostname to TS servers, wait 5 sec for a response, then send results to client
        else:
            
            # Establish TS1 and TS2 sockets and servers
            TS1Server = socketOpen(serverLabelTS1, portTS1)
            TS1Server.connect(socketBind(serverLabelTS1, hostnameTS1, portTS1))
            TS2Server = socketOpen(serverLabelTS2, portTS2)
            TS2Server.connect(socketBind(serverLabelTS2, hostnameTS2, portTS2))
        
            hostnameSentPrompt = "Sending \"" + hostname + "\" to TS1 and TS2 servers...\n"
            print(hostnameSentPrompt)
            
            queueThreadTS1 = queue.Queue()
            queueThreadTS2 = queue.Queue()
            queryThreadTS1 = threading.Thread(name='queryThreadTS1', target = query, args=(TS1Server, hostname, queueThreadTS1,))
            queryThreadTS2 = threading.Thread(name='queryThreadTS2', target = query, args=(TS2Server, hostname, queueThreadTS2,))
            
            queryThreadTS1.start()
            queryThreadTS2.start()

            evaluate(serverLabelTS1, serverLabelTS2, clientConnection, hostname, TS1Server, TS2Server, queueThreadTS1, queueThreadTS2)
            
        # Close the client socket connection
        print("Closing client socket connection.\n\n")
        clientConnection.close()

# server function takes in a given label for the server, a label for the client connecting to it, and labels for the servers that will be connected to.
def server(label, clientLabel, serverLabelTS1, serverLabelTS2):
    
    # Establish LS server port via command-line argument
    port = int(sys.argv[1])
    
    # Establish TS1 hostname via command-line argument
    hostnameTS1 = str(sys.argv[2])
    
    # Establish TS1 server port via command-line argument
    portTS1 = int(sys.argv[3])
    
    # Establish TS2 hostname via command-line argument
    hostnameTS2 = str(sys.argv[4])
    
    # Establish TS2 server port via command-line argument
    portTS2 = int(sys.argv[5])

    # Open client socket and listen
    client = socketOpen(clientLabel, port)
    client.bind(('', port))
    client.listen(1)
    
    # Print out LS's hostname and its respective IP address
    serverInfo(label)
    
    # Set up simultaneous queries to TS servers for each client query
    queryMultiThread(label, clientLabel, client, serverLabelTS1, hostnameTS1, portTS1, serverLabelTS2, hostnameTS2, portTS2)
    
    # Close client socket and shutdown server
    client.close()
    exit()

if __name__ == "__main__":

    # Set label for the servers and client
    label = "LSServer"
    clientLabel = "LSClient"
    serverLabelTS1 = "TS1Server"
    serverLabelTS2 = "TS2Server"
    
    thread = threading.Thread(name='server', target = server, args = (label, clientLabel, serverLabelTS1, serverLabelTS2,))
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\n" + label + " thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)
