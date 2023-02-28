from socket import *    

webserverSocket = socket(AF_INET, SOCK_STREAM)
webserverSocket.bind(("", 6789))
webserverSocket.listen(1)

while True:
        print('Ready to serve...')

        connectionSocket, addr = webserverSocket.accept()

        try:
                # update request with a loop
                request = connectionSocket.recv(8192)

                # Parse
                first_line = request.split(b'\n')[0]
                url = first_line.split()[1]

                filename_pos = url.rfind(b'/')

                filename = url[filename_pos + 1:]

                connectionSocket.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())

                with open(filename, "rb") as file:
                        while True:
                                data = file.read(8192)
                                if(len(data) > 0):
                                        connectionSocket.sendall(data)
                                else:
                                        break


                connectionSocket.sendall("\r\n".encode())

                connectionSocket.close()
        except IOError:
                connectionSocket.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                connectionSocket.sendall("\r\n".encode())
                
                connectionSocket.close()

webserverSocket.close()
