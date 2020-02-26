# Anthony Tiongson
# TS (a simplified top-level DNS server)
# Try to use a dictionary to store data in PROJI-DNSTS.txt
# resources:
#   https://www.pythonforbeginners.com/system/python-sys-argv

import sys, threading, time, random, socket

def server():

    # Establish port via command-line argument
    port = int(sys.argv[1])

    try:
    
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("TS server socket created...")
    except socket.error as socketError:
    
        print('TS socket already open, error: {}\n'.format(socketError))
        exit()
        
    serverBinding = ('', port)
    serverSocket.bind(serverBinding)
    serverSocket.listen(1)
    host = socket.gethostname()
    print("TS server host name: {}".format(host))
    localhostIP = (socket.gethostbyname(host))
    print("TS server IP address: {}".format(localhostIP))
    clientSocketID, address = serverSocket.accept()
    print("Received client connection request from: {}".format(address))
    
    # Server greeting message to client
    greeting = "Welcome to CS 352 TS server! Socket to me!"
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
    
    print("\nTS server thread executed, sleep time: " + str(sleepTime) + " sec\n")
    
    time.sleep(sleepTime)

