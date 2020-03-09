# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# Client side DNS
#
# resources:
#   https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
#   https://www.pythonforbeginners.com/system/python-sys-argv
#   https://www.w3schools.com/python/ref_string_split.asp

import sys, threading, time, socket

def client():

    # Establish LS hostname
    LSHostname = str(sys.argv[1])
    
    # Establish LS port via command-line argument
    LSPort = int(sys.argv[2])
    
    # Create file object to read list of hostnames to query
    hostnameQueryFile = open("PROJ2-HNS.txt", "r")
    
    # Create file object to write all outputs
    results = open("RESOLVED.txt", "a")
    
    # Read a line in the file list of hostnames, connect to LS server, send that hostname to the LS server, wait for a response, commit final responses to the results file, close connection
    for line in hostnameQueryFile:
    
        # Establish LS socket
        try:
        
            clientLSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientLSSocketCreated = "Client socket created to connect to LS server: port " + str(LSPort) + "\n"
            print(clientLSSocketCreated)
        except socket.error as socketError:
        
            socketOpenError = 'LS socket already open, error: {} \n'.format(socketError)
            print(socketOpenError)
            exit()
    
        # Define the IP address on which you want to connect to the LS server
        LSIPAddress = socket.gethostbyname(LSHostname)
        print("Hostname on which to connect to LS server: " + LSHostname + "\n" + "IP address: " + str(LSIPAddress) + "\n")
        LSServerBinding = (LSIPAddress, LSPort)
    
        # Connect to the LS server
        clientLSSocket.connect(LSServerBinding)
    
        hostname = line.splitlines()[0].lower()
        hostnameSentPrompt = "Sending \"" + hostname + "\" to LS server...\n"
        print(hostnameSentPrompt)
        clientLSSocket.send(hostname.encode('utf-8'))
        responseFromServer = clientLSSocket.recv(256)
        responsePrompt = "Response received from the LS server: {}\n".format(responseFromServer.decode('utf-8'))
        print(responsePrompt)
        
        # Close connection to LS socket
        print("Closing LS socket connection.\n")
        clientLSSocket.close()
        
        results.write(responseFromServer + "\n")

    # Tell the server to shut down and close connection
    # Establish LS socket
    try:
    
        clientLSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientLSSocketCreated = "Client socket created to connect to LS server: port " + str(LSPort) + "\n"
        print(clientLSSocketCreated)
    except socket.error as socketError:
    
        socketOpenError = 'LS socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        exit()
        
    # Define the IP address on which you want to connect to the LS server
    LSIPAddress = socket.gethostbyname(LSHostname)
    print("Hostname on which to connect to LS server: " + LSHostname + "\n" + "IP address: " + str(LSIPAddress) + "\n")
    LSServerBinding = (LSIPAddress, LSPort)

    # Connect to the LS server
    clientLSSocket.connect(LSServerBinding)
    
    # Send shutdown command
    print("Shutting down LS server...\n")
    clientLSSocket.send("shutdownLSServer".encode('utf-8'))
    # Close connection to LS socket
    print("Closing LS socket connection.\n")
    clientLSSocket.close()
    
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
