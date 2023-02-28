from socket import *    

proxyserverSocket = socket(AF_INET, SOCK_STREAM)
proxyserverSocket.bind(("", 8888))
proxyserverSocket.listen(1)

while True:
        #implement cache on proxy side so same file retrieves are faster
        print('Ready to serve...')
        
        connectionSocket, addr = proxyserverSocket.accept()

        request = connectionSocket.recv(8192)

        # Parse for port and webserver
        first_line = request.split(b'\n')[0]
        url = first_line.split()[1]

        http_pos = url.find(b'/')
        temp = url[(http_pos + 1):]

        webserver_pos = temp.find(b'/')
        port_pos = temp.find(b':')

        webserver = temp[:port_pos]
        port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
                
        webserverSocket = socket(AF_INET, SOCK_STREAM)
        webserverSocket.connect((webserver, port))
        webserverSocket.sendall(request)

        while True:
                data = webserverSocket.recv(8192)
                if(len(data) > 0):
                        connectionSocket.sendall(data)
                else:
                        break

        webserverSocket.close()
        connectionSocket.close()

proxyserverSocket.close()
