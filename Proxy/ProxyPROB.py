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

                port_start_pos = url.find(b':')
        
                port_end_pos = url.rfind(b'/')
                        
                webserver = url[1:port_start_pos]

                port = int(url[port_start_pos+1:port_end_pos])

                filename = url[port_end_pos+1:]

                try:
                        with open(filename, "rb") as file:
                                connectionSocket.sendall(file.read())
                except IOError:
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
                        
                        with open(filename, "wb") as file:
                                file.write(data)

                        connectionSocket.sendall(data)

                        webserverSocket.close()

                connectionSocket.close()

        except:
                connectionSocket.close()

proxyserverSocket.close()
