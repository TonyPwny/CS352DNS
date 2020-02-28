# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# Client side DNS
# resources:
#   https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
#   https://www.pythonforbeginners.com/system/python-sys-argv
#   https://www.w3schools.com/python/ref_string_split.asp

import sys, threading, time, random, socket

def client():

    # Establish RS hostname
    RSHostname = str(sys.argv[1])
    
    # Establish RS and TS server port via command-line argument
    RSPort = int(sys.argv[2])
    TSPort = int(sys.argv[3])
    
    # Create file object to read list of hostnames to query
    hostnameQueryFile = open("PROJI-HNS.txt", "r")
    
    # Create file object to write all outputs
    results = open("RESOLVED.txt", "a")
    
    # Read a line in the file list of hostnames, connect to RS server, send that hostname to the RS server, wait for a response, reevaluate response, commit final responses to the results file, close connection
    for line in hostnameQueryFile:
    
        # Establish RS socket
        try:
        
            clientRSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientRSSocketCreated = "Client socket created to connect to RS server: port " + str(RSPort) + "\n"
            print(clientRSSocketCreated)
        except socket.error as socketError:
        
            socketOpenError = 'RS socket already open, error: {} \n'.format(socketError)
            print(socketOpenError)
            exit()
    
        # Define the IP address on which you want to connect to the RS server
        RSIPAddress = socket.gethostbyname(RSHostname)
        print("Hostname on which to connect to RS server: " + RSHostname + "\n" + "IP address: " + str(RSIPAddress) + "\n")
        RSServerBinding = (RSIPAddress, RSPort)
    
        # Connect to the RS server
        clientRSSocket.connect(RSServerBinding)
        
        # Receive greeting from the RS server
        greetingFromRSServer = clientRSSocket.recv(64)
        RSGreeting = "Greeting received from the RS server: {}\n".format(greetingFromRSServer.decode('utf-8'))
        print(RSGreeting)
    
        hostname = line.splitlines()[0].lower()
        hostnameSentPrompt = "Sending \"" + hostname + "\" to RS server...\n"
        print(hostnameSentPrompt)
        clientRSSocket.send(hostname.encode('utf-8'))
        responseFromServer = clientRSSocket.recv(256)
        responsePrompt = "Response received from the RS server: {}\n".format(responseFromServer.decode('utf-8'))
        print(responsePrompt)
        
        # Close connection to RS socket
        print("Closing RS socket connection.\n")
        clientRSSocket.close()
        
        if responseFromServer.split()[2] == "NS":
        
            # Establish TS socket
            try:
            
                clientTSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientTSSocketCreated = "Client socket created to connect to TS server: port " + str(TSPort) + "\n"
                print(clientTSSocketCreated)
            except socket.error as socketError:
            
                socketOpenError = 'TS socket already open, error: {} \n'.format(socketError)
                print(socketOpenError)
                exit()
        
            TSHostname = responseFromServer.split()[0]
            TSIPAddress = (socket.gethostbyname(TSHostname))
        
            TSServerBinding = (TSIPAddress, TSPort)
            clientTSSocket.connect(TSServerBinding)
            greetingFromTSServer = clientTSSocket.recv(64)
            TSGreeting = "Greeting received from the TS server: {}\n".format(greetingFromTSServer.decode('utf-8'))
            print(TSGreeting)

            hostnameRedirectPrompt = "Redirecting \"" + hostname + "\" to TS server: " + TSHostname + "\n" + "IP Address: " + TSIPAddress + "\n"
            print(hostnameRedirectPrompt)
            clientTSSocket.send(hostname.encode('utf-8'))
            responseFromServer = clientTSSocket.recv(256)
            responsePrompt = "Response received from the TS server: {}\n".format(responseFromServer.decode('utf-8'))
            print(responsePrompt)
            
            # Close connection to TS server
            print("Closing TS socket connection.\n")
            clientTSSocket.close()
            
        
        results.write(responseFromServer + "\n")

    # Tell the servers to shut down and close connection
    # Establish RS socket
    try:
    
        clientRSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientRSSocketCreated = "Client socket created to connect to RS server: port " + str(RSPort) + "\n"
        print(clientRSSocketCreated)
    except socket.error as socketError:
    
        socketOpenError = 'RS socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        exit()
        
    # Define the IP address on which you want to connect to the RS server
    RSIPAddress = socket.gethostbyname(RSHostname)
    print("Hostname on which to connect to RS server: " + RSHostname + "\n" + "IP address: " + str(RSIPAddress) + "\n")
    RSServerBinding = (RSIPAddress, RSPort)

    # Connect to the RS server
    clientRSSocket.connect(RSServerBinding)
    
    # Receive greeting from the RS server
    greetingFromRSServer = clientRSSocket.recv(64)
    RSGreeting = "Greeting received from the RS server: {}\n".format(greetingFromRSServer.decode('utf-8'))
    print(RSGreeting)
        
    # Establish TS socket
    try:
    
        clientTSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientTSSocketCreated = "Client socket created to connect to TS server: port " + str(TSPort) + "\n"
        print(clientTSSocketCreated)
    except socket.error as socketError:
    
        socketOpenError = 'TS socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        exit()
        
    TSIPAddress = (socket.gethostbyname(TSHostname))

    TSServerBinding = (TSIPAddress, TSPort)
    clientTSSocket.connect(TSServerBinding)
    greetingFromTSServer = clientTSSocket.recv(64)
    TSGreeting = "Greeting received from the TS server: {}\n".format(greetingFromTSServer.decode('utf-8'))
    print(TSGreeting)
    
    # Send shutdown command
    print("Shutting down RS and TS servers...\n")
    clientRSSocket.send("shutdownRSServer".encode('utf-8'))
    clientTSSocket.send("shutdownTSServer".encode('utf-8'))
    # Close connection to RS socket
    print("Closing RS socket connection.\n")
    clientRSSocket.close()
    # Close connection to TS socket
    print("Closing TS socket connection.\n")
    clientTSSocket.close()
    
    
    # Close all files and shutdown client
    hostnameQueryFile.close()
    results.close()
    exit()

if __name__ == "__main__":
    
    thread = threading.Thread(name='client', target = client)
    thread.start()
    
    sleepTime = 5
    
    executionPrompt = "\nClient thread executed, sleep time: " + str(sleepTime) + " sec\n"
    print(executionPrompt)
    
    time.sleep(sleepTime)

