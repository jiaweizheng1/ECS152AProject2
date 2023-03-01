from socket import *    

proxyserverSocket = socket(AF_INET, SOCK_STREAM)
proxyserverSocket.bind(("", 8888))
proxyserverSocket.listen(1)

while True:
        print('Ready to serve...')

        connectionSocket, addr = proxyserverSocket.accept()

        try:
                request = connectionSocket.recv(8192)

                first_line = request.split(b'\n')[0]

                url = first_line.split()[1]
        
                port_end_pos = url.rfind(b'/')

                filename = url[port_end_pos+1:]

                try:
                        existingfile = open(filename, "rb")

                        connectionSocket.sendall(existingfile.read())

                        existingfile.close()
                except IOError:
                        port_start_pos = url.find(b':')
                        
                        webserver = url[1:port_start_pos]

                        port = int(url[port_start_pos+1:port_end_pos])
                        
                        webserverSocket = socket(AF_INET, SOCK_STREAM)
                        
                        webserverSocket.connect((webserver, port))

                        webserverSocket.sendall(request)

                        data = []
                        
                        while True:
                                data_buff = webserverSocket.recv(8192)
                                if not data_buff:
                                        break
                                data.append(data_buff)

                        data = b''.join(data)

                        if b'200 OK' in data:
                                newfile = open(filename, "wb")

                                newfile.write(data)

                                newfile.close()

                        connectionSocket.sendall(data)

                        webserverSocket.close()

                connectionSocket.close()

        except:
                connectionSocket.close()

proxyserverSocket.close()
