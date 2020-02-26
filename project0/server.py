# Anthony Tiongson

import threading, time, random, socket

def server():

    try:
    
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server socket created...")
    except socket.error as socketError:
    
        print('Socket already open, error: {}\n'.format(socketError))
        exit()
        
    serverBinding = ('', 57777)
    serverSocket.bind(serverBinding)
    serverSocket.listen(1)
    host = socket.gethostname()
    print("Server host name: {}".format(host))
    localhostIP = (socket.gethostbyname(host))
    print("Server IP address: {}".format(localhostIP))
    clientSocketID, address = serverSocket.accept()
    print("Received client connection request from: {}".format(address))
    
    # Server greeting message to client
    greeting = "Welcome to CS 352! Socket to me!"
    clientSocketID.send(greeting.encode('utf-8'))
    
    # Receive message from the client
    dataFromClient = clientSocketID.recv(100)
    
    # Send back message, but in reverse
    clientSocketID.send(dataFromClient[::-1].encode('utf-8'))
    
    # Close the server socket
    serverSocket.close()
    exit()

if __name__ == "__main__":

    thread = threading.Thread(name='server', target = server)
    thread.start()
    
    sleepTime = random.random() * 5
    
    print("\nServer thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)
