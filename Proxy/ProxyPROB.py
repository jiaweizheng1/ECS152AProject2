from socket import *    

# Create a TCP server socket
proxyserverSocket = socket(AF_INET, SOCK_STREAM)
proxyserverSocket.bind(("", 8888))
proxyserverSocket.listen(1)

while True:
        print('Ready to serve...')
        # Set up a new connection from the client
        connectionSocket, addr = proxyserverSocket.accept()

        try:
                # Receives the request message from the client
                request = connectionSocket.recv(8192)
                
                # Getting url from the message
                first_line = request.split(b'\n')[0]
                url = first_line.split()[1]

                # Getting filename from the url
                port_end_pos = url.rfind(b'/')
                filename = url[port_end_pos+1:]

                try:    
                        # Try to open file directly from cache
                        existingfile = open(filename, "rb")

                        print("got " + filename.decode() + " from cache")

                        # If success, just send cache data to the client
                        connectionSocket.sendall(existingfile.read())

                        existingfile.close()
                except IOError:
                        print("got " + filename.decode() + " from web server")
                        
                        # If there was no required file in cache, set up 
                        # connection with the web server
                        port_start_pos = url.find(b':')

                        # Getting server's ip
                        webserver = url[1:port_start_pos]

                        # Getting port number
                        port = int(url[port_start_pos+1:port_end_pos])
                        
                        # Set up connection and send requests
                        webserverSocket = socket(AF_INET, SOCK_STREAM)
                        webserverSocket.connect((webserver, port))
                        webserverSocket.sendall(request)

                        data = []
                        while True:
                                # Saving data temporarily
                                data_buff = webserverSocket.recv(8192)
                                if not data_buff:
                                        break
                                data.append(data_buff)
                        data = b''.join(data)
                        
                        # If the data is valid, save in the cache
                        if b'200 OK' in data:
                                newfile = open(filename, "wb")
                                newfile.write(data)
                                newfile.close()
                                
                        # Send the data to the client
                        connectionSocket.sendall(data)

                        webserverSocket.close()

                connectionSocket.close()
        except:
                connectionSocket.close()

proxyserverSocket.close()
