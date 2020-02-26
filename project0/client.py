# Anthony Tiongson
# resources: https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

import threading, time, random, socket

def client():

    # Create file object to write all outputs
    fileOutput = open("out-proj0.txt", "a")
    
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocketCreated = "Client socket created...\n"
        print(clientSocketCreated)
        fileOutput.write(clientSocketCreated)
    except socket.error as socketError:
        socketOpenError = 'Socket already open, error: {} \n'.format(socketError)
        print(socketOpenError)
        fileOutput.write(socketOpenError)
        exit()
    
    # Define the port on which you want to connect to the server
    port = 57777
    localhostAddress = socket.gethostbyname(socket.gethostname())
    
    # Connect to the server on local machine
    serverBinding = (localhostAddress, port)
    clientSocket.connect(serverBinding)
    
    # Receive greeting from the server
    dataFromServer = clientSocket.recv(100)
    greetingReceived = "Greeting received from the server: {}\n".format(dataFromServer.decode('utf-8'))
    print(greetingReceived)
    fileOutput.write(greetingReceived)
    
    # Send a message to the server
    message = "Hello! Can you slice?"
    messageSentPrompt = "Sending \"" + message + "\" to server...\n"
    print(messageSentPrompt)
    fileOutput.write(messageSentPrompt)
    clientSocket.send(message.encode('utf-8'))
    
    # Receive response from the server
    dataFromServer = clientSocket.recv(100)
    responsePrompt = "Response received from the server: {}\n".format(dataFromServer.decode('utf-8'))
    print(responsePrompt)
    fileOutput.write(responsePrompt)
    
    # Open a local file, read it and append to file output
    fileRead = open("in-proj0.txt", "r")
    
    for line in fileRead:
        print(line)
        fileOutput.write(line)
    
    # Close the client socket
    clientSocket.close()
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
