# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# LS (a simplified load-balancing DNS server)
#    The LS receives queries from the client and forwards them directly to
#    both TS1 and TS2.
#
#    Since the DNS tables for TS1 and TS2 have no overlap, at most one will
#    respond to any query. It is possible that neither of them responds.
#
#    If the LS receives a response from one of the TS servers, it should
#    just forward the response as is to the client. (As shown above, this
#    string will have the format
#
#    Hostname IPaddress A
#
#    as obtained from the TS that just responded.)
#
#    If the LS does not receive a response from either TS within a time
#    interval of 5 seconds (OK to wait slightly longer), the LS must send
#    the client the message
#
#    Hostname - Error:HOST NOT FOUND
#
#    where the Hostname is the client-requested host name.
#
#    The LS maintains three connections (and sockets): one with the client,
#    and one with each TS server.
#
#    The most tricky part of implementing the LS is figuring out which TS
#    has pushed data into its corresponding socket (if at all one of them
#    has), and timing out when neither has pushed data. Think carefully
#    about how you will achieve this. Just performing recv() calls on the
#    two TS sockets won't do it, since recv() by default is a __blocking
#    call__: if you recv() on the TS1 socket but TS1 hasn't pushed any
#    data, your LS program will indefinitely hang.
#
#    python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort
#    - ts1ListenPort and ts2ListenPort are ports accepting incoming connections
#      at TS1 and TS2 (resp.) from LS
#    - lsListenPort is the port accepting incoming connections from the
#      client at LS
#
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv
#   https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
#   https://stackoverflow.com/questions/13941562/why-can-i-not-catch-a-queue-empty-exception-from-a-multiprocessing-queue/13941865

import queue, random, socket, sys, threading, time

def query(clientSocket, hostname, queue):
    
    clientSocket.settimeout(5)
    clientSocket.send(hostname.encode('utf-8'))
    try:
    
        responseFromServer = clientSocket.recv(256).decode('utf-8')
        queue.put(responseFromServer)
    except socket.timeout, queryTimeout:

        responseFromServer = str(queryTimeout)
        queue.put(responseFromServer)
    except socket.error, queryError:
    
        # Something else happened, handle error, exit, etc.
        print queryError
        sys.exit(1)

def server():
    
    # Establish LS server port via command-line argument
    LSPort = int(sys.argv[1])
    
    # Establish TS1 hostname via command-line argument
    TS1Hostname = str(sys.argv[2])
    
    # Establish TS1 server port via command-line argument
    TS1Port = int(sys.argv[3])
    
    # Establish TS2 hostname via command-line argument
    TS2Hostname = str(sys.argv[4])
    
    # Establish TS2 server port via command-line argument
    TS2Port = int(sys.argv[5])

    # Establish LS server socket
    try:
    
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("LS server socket created: port " + str(LSPort) + "\n")
    except socket.error as socketError:
    
        print('LS socket already open, error: {}\n'.format(socketError))
        exit()
        
    serverBinding = ('', LSPort)
    serverSocket.bind(serverBinding)
    serverSocket.listen(1)
    LSHostname = socket.gethostname()
    print("LS server hostname: {}".format(LSHostname))
    localhostIP = (socket.gethostbyname(LSHostname))
    print("LS server IP address: {}".format(localhostIP))
    
    while True:
    
        clientSocketID, address = serverSocket.accept()
        print("Received client connection request from: {}".format(address))
    
        # Receive hostname query from the client
        hostname = clientSocketID.recv(256)
    
        # The client is done querying
        if hostname == "shutdownLSServer":
        
            print("Received shutdown command...")
            
            # Tell the TS1 server to shut down and close connection
            # Establish TS1 socket
            try:
            
                clientTS1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientTS1SocketCreated = "Client socket created to connect to TS1 server: port " + str(TS1Port) + "\n"
                print(clientTS1SocketCreated)
            except socket.error as socketError:
            
                socketOpenError = 'TS1 socket already open, error: {} \n'.format(socketError)
                print(socketOpenError)
                exit()
                
            # Define the IP address on which you want to connect to the TS1 server
            TS1IPAddress = socket.gethostbyname(TS1Hostname)
            print("Hostname on which to connect to TS1 server: " + TS1Hostname + "\n" + "IP address: " + str(TS1IPAddress) + "\n")
            TS1ServerBinding = (TS1IPAddress, TS1Port)

            # Connect to the LS server
            clientTS1Socket.connect(TS1ServerBinding)
            
            # Send shutdown command
            print("Shutting down TS1 server...\n")
            clientTS1Socket.send("shutdownTSServer".encode('utf-8'))
            # Close connection to LS socket
            print("Closing TS1 socket connection.\n")
            clientTS1Socket.close()
            
            # Tell the TS2 server to shut down and close connection
            # Establish TS2 socket
            try:
            
                clientTS2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientTS2SocketCreated = "Client socket created to connect to TS2 server: port " + str(TS2Port) + "\n"
                print(clientTS2SocketCreated)
            except socket.error as socketError:
            
                socketOpenError = 'TS2 socket already open, error: {} \n'.format(socketError)
                print(socketOpenError)
                exit()
                
            # Define the IP address on which you want to connect to the TS2 server
            TS2IPAddress = socket.gethostbyname(TS2Hostname)
            print("Hostname on which to connect to TS2 server: " + TS2Hostname + "\n" + "IP address: " + str(TS2IPAddress) + "\n")
            TS2ServerBinding = (TS2IPAddress, TS2Port)

            # Connect to the TS2 server
            clientTS2Socket.connect(TS2ServerBinding)
            
            # Send shutdown command
            print("Shutting down TS2 server...\n")
            clientTS2Socket.send("shutdownTSServer".encode('utf-8'))
            # Close connection to LS socket
            print("Closing TS2 socket connection.\n")
            clientTS2Socket.close()
            
            break
        # Send hostname to TS servers, wait 5 sec for a response, then send results to client
        else:
        
            # Establish TS1 socket and server
            try:
            
                clientTS1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientTS1SocketCreated = "Client socket created to connect to TS1 server: port " + str(TS1Port) + "\n"
                print(clientTS1SocketCreated)
            except socket.error as socketError:
            
                socketOpenError = 'TS1 socket already open, error: {} \n'.format(socketError)
                print(socketOpenError)
                exit()
        
            # Define the IP address on which you want to connect to the TS1 server
            TS1IPAddress = socket.gethostbyname(TS1Hostname)
            print("Hostname on which to connect to TS1 server: " + TS1Hostname + "\n" + "IP address: " + str(TS1IPAddress) + "\n")
            TS1ServerBinding = (TS1IPAddress, TS1Port)
        
            # Connect to the TS1 server
            clientTS1Socket.connect(TS1ServerBinding)
            
            # Establish TS2 socket and server
            try:
            
                clientTS2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientTS2SocketCreated = "Client socket created to connect to TS2 server: port " + str(TS2Port) + "\n"
                print(clientTS2SocketCreated)
            except socket.error as socketError:
            
                socketOpenError = 'TS2 socket already open, error: {} \n'.format(socketError)
                print(socketOpenError)
                exit()
        
            # Define the IP address on which you want to connect to the TS1 server
            TS2IPAddress = socket.gethostbyname(TS2Hostname)
            print("Hostname on which to connect to TS2 server: " + TS2Hostname + "\n" + "IP address: " + str(TS2IPAddress) + "\n")
            TS2ServerBinding = (TS2IPAddress, TS2Port)
        
            # Connect to the TS2 server
            clientTS2Socket.connect(TS2ServerBinding)
        
            hostnameSentPrompt = "Sending \"" + hostname + "\" to TS1 and TS2 servers...\n"
            print(hostnameSentPrompt)
            
            queueThread_1 = queue.Queue()
            queueThread_2 = queue.Queue()
            queryThread_1 = threading.Thread(name='queryThreadTS1', target = query, args=(clientTS1Socket, hostname, queueThread_1,))
            queryThread_2 = threading.Thread(name='queryThreadTS2', target = query, args=(clientTS2Socket, hostname, queueThread_2,))
            
            queryThread_1.start()
            queryThread_2.start()
            responseFromTS1Server = None
            responseFromTS2Server = None

            while True:
                
                try:
                
                    responseFromTS1Server = queueThread_1.get_nowait()
                except queue.Empty:
                    
                    pass
                    
                try:
                
                    responseFromTS2Server = queueThread_2.get_nowait()
                except queue.Empty:
                
                    pass
                    
                if responseFromTS1Server is not None and responseFromTS1Server != "timed out":
                    
                    print("Popped " + responseFromTS1Server + " from queue 1.\n")
                    responseTS1Prompt = "Response received from the TS1 server: {}\n".format(responseFromTS1Server)
                    print(responseTS1Prompt)
                    clientSocketID.send(responseFromTS1Server.encode('utf-8'))
                    print("Closing TS1 and TS2 socket connections.\n")
                    clientTS1Socket.close()
                    clientTS2Socket.close()
                    break
                elif responseFromTS2Server is not None and responseFromTS2Server != "timed out":
                
                    print("Popped " + responseFromTS2Server + " from queue 2.\n")
                    responseTS2Prompt = "Response received from the TS2 server: {}\n".format(responseFromTS2Server)
                    print(responseTS2Prompt)
                    clientSocketID.send(responseFromTS2Server.encode('utf-8'))
                    print("Closing TS1 and TS2 socket connections.\n")
                    clientTS1Socket.close()
                    clientTS2Socket.close()
                    break
                elif responseFromTS1Server == "timed out" and responseFromTS2Server == "timed out":
                
                    noResponse = hostname + " - Error:HOST NOT FOUND"
                    clientSocketID.send(noResponse.encode('utf-8'))
                    print("TS1 and TS2 timeout...")
                    print("Closing TS1 and TS2 socket connections.\n")
                    clientTS1Socket.close()
                    clientTS2Socket.close()
                    break
            
        # Close the client socket connection
        print("\nClosing client socket connection.\n")
        clientSocketID.close()
    
    # Close server socket and shutdown server
    serverSocket.close()
    exit()

if __name__ == "__main__":

    thread = threading.Thread(name='server', target = server)
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\nLS server thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)

