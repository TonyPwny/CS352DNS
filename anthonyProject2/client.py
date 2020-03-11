# Anthony Tiongson (ast119) with assistance from Nicolas Gundersen (neg62)
# Client side DNS
#
# resources:
#   https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
#   https://www.pythonforbeginners.com/system/python-sys-argv
#   https://www.w3schools.com/python/ref_string_split.asp
#   https://www.geeksforgeeks.org/args-kwargs-python/

import socket, sys, threading, time

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

# queryFile function connects to a server of a given hostname and port designated by a label and reads a given file input of queries to send to the server.  The result of each the query is then written to a given file output.
def queryFile(label, hostname, port, input, output):

    # Read a line from an input file list of hostnames, connect to a server, send that hostname to the server, close connection after receiving a response, commit results to an output file.
    for line in input:
    
        # Open server socket.
        server = socketOpen(label, port)
    
        # Create server socketBind and connect to the server.
        server.connect(socketBind(label, hostname, port))
    
        query = line.splitlines()[0].lower()
        querySentPrompt = "Sending \"" + query + "\" to " + label + "...\n"
        print(querySentPrompt)
        server.send(query.encode('utf-8'))
        responseFromServer = server.recv(256)
        responsePrompt = "Response received from the " + label + ": {}\n".format(responseFromServer.decode('utf-8'))
        print(responsePrompt)
        
        # Close connection to server socket.
        print("Closing " + label + " socket connection.\n")
        server.close()
        
        output.write(responseFromServer + "\n")
    
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
    
# shutdown function closes given files and shuts down the client.
def shutdown(*files):

    print("Closing files...")
    
    for file in files:
    
        file.close()
        
    print("Shutting down client.")
    exit()

def client(serverLabel, hostnameQueryFile, results):

    # Establish server hostname.
    hostname = str(sys.argv[1])
    
    # Establish server port via command-line argument.
    port = int(sys.argv[2])
    
    # Read all hostnames in hostnameQueryFile to query the server and write responses in the file results.
    queryFile(serverLabel, hostname, port, hostnameQueryFile, results)

    # Send shutdown command to server once file is completely queried.
    shutdownServer(serverLabel, hostname, port)
    
    # Close all files and shutdown client.
    shutdown(hostnameQueryFile, results)

if __name__ == "__main__":
    
    # Set label for server client will connect to
    serverLabel = "LSServer"
    
    # Create file object to read list of hostnames to query.
    hostnameQueryFile = open("PROJ2-HNS.txt", "r")
    
    # Create file object to write all outputs.
    results = open("RESOLVED.txt", "a")
    
    thread = threading.Thread(name='client', target = client, args = (serverLabel, hostnameQueryFile, results,))
    thread.start()
    
    sleepTime = 5
    
    executionPrompt = "\nClient thread executed, sleep time: " + str(sleepTime) + " sec\n"
    print(executionPrompt)
    
    time.sleep(sleepTime)
