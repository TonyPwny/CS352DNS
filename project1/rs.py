# Anthony Tiongson
# RS (a simplified root DNS server)
# Try to use a dictionary to store data in PROJI-DNSRS.txt
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv

import sys, threading, time, random, socket

def server():
    
    # Establish port via command-line argument
    port = int(sys.argv[1])
    
    try:
    
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("RS server socket created...")
    except socket.error as socketError:
    
        print('RS socket already open, error: {}\n'.format(socketError))
        exit()
        
    serverBinding = ('', port)
    serverSocket.bind(serverBinding)
    serverSocket.listen(1)
    host = socket.gethostname()
    print("RS server host name: {}".format(host))
    localhostIP = (socket.gethostbyname(host))
    print("RS server IP address: {}".format(localhostIP))
    clientSocketID, address = serverSocket.accept()
    print("Received client connection request from: {}".format(address))
    
    # Server greeting message to client
    greeting = "Welcome to CS 352 RS server! Socket to me!"
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
    
    print("\nRS server thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)

