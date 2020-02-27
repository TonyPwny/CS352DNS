# Anthony Tiongson
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
    
    # Establish RS socket
    try:
    
        clientRSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientRSSocketCreated = "Client socket created to connect to RS server: port " + str(RSPort) + "\n"
        print(clientRSSocketCreated)
    except socket.error as socketError:
    
        socketOpenError = 'RS socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        exit()
    
    # Establish TS socket
    try:
    
        clientTSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientTSSocketCreated = "Client socket created to connect to TS server: port " + str(TSPort) + "\n"
        print(clientTSSocketCreated)
    except socket.error as socketError:
    
        socketOpenError = 'TS socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        exit()
    
    # Define the IP address on which you want to connect to the RS server
    RSIPAddress = socket.gethostbyname(RSHostname)
    print("Hostname on which to connect to RS server: " + RSHostname + "\n" + "IP address: " + str(RSIPAddress) + "\n")
    
    # Connect to the RS server on local machine
    RSServerBinding = (RSIPAddress, RSPort)
    clientRSSocket.connect(RSServerBinding)
    
    # Receive greeting from the RS server
    greetingFromRSServer = clientRSSocket.recv(64)
    RSGreeting = "Greeting received from the RS server: {}\n".format(greetingFromRSServer.decode('utf-8'))
    print(RSGreeting)
    
    # Query for TS server hostname
    TSQueryPrompt = "Querying for TS server hostname...\n"
    print(TSQueryPrompt)
    clientRSSocket.send("whatIsTheTSHostname".encode('utf-8'))
    TSQueryResponse = clientRSSocket.recv(64)
    TSHostname = TSQueryResponse.split()[0]
    TSIPAddress = (socket.gethostbyname(TSHostname))
    
    TSServerBinding = (TSIPAddress, TSPort)
    clientTSSocket.connect(TSServerBinding)
    greetingFromTSServer = clientTSSocket.recv(64)
    TSGreeting = "Greeting received from the TS server: {}\n".format(greetingFromTSServer.decode('utf-8'))
    print(TSGreeting)
    
    # Read each line in the file list of hostnames, send each hostname to the RS server, wait for a response, reevaluate response, commit final responses to the results file
    for line in hostnameQueryFile:
    
        hostname = line.splitlines()[0].lower()
        hostnameSentPrompt = "Sending \"" + hostname + "\" to RS server...\n"
        print(hostnameSentPrompt)
        clientRSSocket.send(hostname.encode('utf-8'))
        responseFromServer = clientRSSocket.recv(64)
        responsePrompt = "Response received from the RS server: {}\n".format(responseFromServer.decode('utf-8'))
        print(responsePrompt)
        
        if responseFromServer.split()[2] == "NS":

            hostnameRedirectPrompt = "Redirecting \"" + hostname + "\" to TS server: " + TSHostname + "\n" + "IP Address: " + TSIPAddress + "\n"
            print(hostnameRedirectPrompt)
            clientTSSocket.send(hostname.encode('utf-8'))
            responseFromServer = clientTSSocket.recv(64)
            responsePrompt = "Response received from the TS server: {}\n".format(responseFromServer.decode('utf-8'))
            print(responsePrompt)
            
        
        results.write(responseFromServer + "\n")

    # Tell the server's your'e done
    clientRSSocket.send("EndOfQuery".encode('utf-8'))
    clientTSSocket.send("EndOfQuery".encode('utf-8'))
    
    
    # Close the client socket
    clientRSSocket.close()
    clientTSSocket.close()
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

