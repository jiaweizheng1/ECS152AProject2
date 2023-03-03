from socket import *

# Create a TCP socket on port 6789 for web server
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
webserverSocket = socket(AF_INET, SOCK_STREAM)
webserverSocket.bind((gethostbyname(gethostname()), 6789))
webserverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
        print('Ready to serve...')
        
        # Set up a new connection from the client
        connectionSocket, addr = webserverSocket.accept()

        try:
                # Receives the request message from the client
                request = connectionSocket.recv(8192)

                # get only the first line in request
                # ex: "GET /helloworld.html HTTP/1.1"
                first_line = request.split(b'\n')[0]

                # get only the url or path name
                # ex: "/helloworld.html"
                url = first_line.split()[1]

                # get position of last '/' character 
                filename_pos = url.rfind(b'/')

                # extract file name using last '/' position
                # ex: "helloworld.html"
                filename = url[filename_pos+1:]

                # open that file in the current directory
                existingfile = open(filename, "rb")

                # Send the HTTP response header line to the connection socket
                connectionSocket.sendall(b'HTTP/1.1 200 OK\r\n\r\n')

                # Send the content of the requested file to the connection socket
                connectionSocket.sendall(existingfile.read())

                print("read from file " + filename.decode())

                # send trailer
                connectionSocket.sendall(b'\r\n')

                # close opened file
                existingfile.close()

                # Close the client connection socket
                connectionSocket.close()
                
        except:
                # Send HTTP response message for file not found
                connectionSocket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')

                print("dont have file " + filename.decode())

                # Close the client connection socket
                connectionSocket.close()

webserverSocket.close()
