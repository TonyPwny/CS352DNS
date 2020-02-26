# Anthony Tiongson
# Client side DNS
# resources:
#   https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
#   https://www.pythonforbeginners.com/system/python-sys-argv

import sys, threading, time, random, socket

def client():

    # Establish RS and TS server port via command-line argument
    RSPort = int(sys.argv[1])
    TSPort = int(sys.argv[2])
    
    # Create file object to write all outputs
    fileOutput = open("out-proj0.txt", "a")
    
    try:
        clientRSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientRSSocketCreated = "Client socket created to connect to RS server...\n"
        print(clientRSSocketCreated)
        fileOutput.write(clientRSSocketCreated)
    except socket.error as socketError:
        socketOpenError = 'RS socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        fileOutput.write(socketOpenError)
        exit()
        
    try:
        clientTSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientTSSocketCreated = "Client socket created to connect to TS server...\n"
        print(clientTSSocketCreated)
        fileOutput.write(clientTSSocketCreated)
    except socket.error as socketError:
        socketOpenError = 'TS socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        fileOutput.write(socketOpenError)
        exit()
    
    # Define the port on which you want to connect to the server
    localhostAddress = socket.gethostbyname(socket.gethostname())
    
    # Connect to the RS server on local machine
    RSServerBinding = (localhostAddress, RSPort)
    clientRSSocket.connect(RSServerBinding)
    
    # Receive greeting from the server
    dataFromServer = clientRSSocket.recv(100)
    greetingReceived = "Greeting received from the server: {}\n".format(dataFromServer.decode('utf-8'))
    print(greetingReceived)
    fileOutput.write(greetingReceived)
    
    # Send a message to the server
    message = "Hello! Can you slice?"
    messageSentPrompt = "Sending \"" + message + "\" to server...\n"
    print(messageSentPrompt)
    fileOutput.write(messageSentPrompt)
    clientRSSocket.send(message.encode('utf-8'))
    
    # Receive response from the server
    dataFromServer = clientRSSocket.recv(100)
    responsePrompt = "Response received from the server: {}\n".format(dataFromServer.decode('utf-8'))
    print(responsePrompt)
    fileOutput.write(responsePrompt)
    
    # Open a local file, read it and append to file output
    fileRead = open("in-proj0.txt", "r")
    
    for line in fileRead:
        print(line)
        fileOutput.write(line)
    
    # Close the client socket
    clientRSSocket.close()
    clientTSSocket.close()
    fileOutput.close()
    exit()

if __name__ == "__main__":

    fileOutput = open("out-proj0.txt", "a")
    
    thread = threading.Thread(name='client', target = client)
    thread.start()
    
    sleepTime = 5
    
    executionPrompt = "\nClient thread executed, sleep time: " + str(sleepTime) + " sec\n"
    print(executionPrompt)
    fileOutput.write(executionPrompt)
    fileOutput.close()
    
    time.sleep(sleepTime)

