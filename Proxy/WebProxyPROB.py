from socket import *    

proxyserverSocket = socket(AF_INET, SOCK_STREAM)
proxyserverSocket.bind(("", 8888))
proxyserverSocket.listen(1)

while True:
                print('Ready to serve...')
        
                connectionSocket, addr = proxyserverSocket.accept()

                webserverSocket = socket(AF_INET, SOCK_STREAM)

                try:
                        request = connectionSocket.recv(1048576)

                        first_line = request.split(b'\n')[0]
        
                        url = first_line.split()[1]

                        first_colon_pos = url.find(b':')
                
                        last_slash_pos = url.rfind(b'/')

                        port = 80
                        
                        # external web server, two situations: from cache vs retrieve and add to cache
                        if url.find(b'://') != -1 or first_colon_pos == -1:
                                webserver = url[last_slash_pos+1:]
                                
                                first_period_pos = webserver.find(b'.')
                                
                                second_period_pos = webserver.rfind(b'.')

                                if first_period_pos != second_period_pos:
                                    webserver = webserver[first_period_pos+1:]

                                try:
                                        with open(webserver, "rb") as file:
                                                connectionSocket.sendall(file.read())
                                except IOError:
                                        request = b'GET http://' +  webserver + b' HTTP/1.1\n\n'
                        
                                        webserverSocket.connect((webserver, port))
                                
                                        webserverSocket.sendall(request)

                                        data = webserverSocket.recv(1048576)

                                        with open(webserver, "wb") as file:
                                                file.write(data)

                                        connectionSocket.sendall(data)

                                webserverSocket.close()
                                
                                connectionSocket.close()
                        # using our web server, two situations: from cache vs retrieve and add to cache
                        else:
                                webserver = url[1:first_colon_pos]

                                port = int(url[first_colon_pos+1:last_slash_pos])

                                filename = url[last_slash_pos+1:]

                                try:
                                        with open(filename, "rb") as file:
                                                connectionSocket.sendall(file.read())
                                except IOError:
                                        webserverSocket.connect((webserver, port))

                                        webserverSocket.sendall(request)

                                        data = webserverSocket.recv(1048576)
                                        
                                        with open(filename, "wb") as file:
                                                file.write(data)

                                        connectionSocket.sendall(data)

                                webserverSocket.close()

                                connectionSocket.close()

                except:
                        webserverSocket.close()
                        
                        connectionSocket.close()

proxyserverSocket.close()
