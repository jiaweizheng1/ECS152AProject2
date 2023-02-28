# Import socket module
from socket import *

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverip = ''
serverport = 8888
serverSocket.bind((serverip, serverport))
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	try:
		# Receives the request message from the client
		message = connectionSocket.recv(1024).decode()
		
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		realdest = message.split()[1]
		realdest = realdest[1:] # remove '/' at the beginning
		pathindex = realdest.find('/') # find if there is a path
		if(pathindex == -1): # if there is no path, simply set as a '/'
			path = '/'
		else:
			path = realdest[pathindex:] # if there is, save the '/[PATH]'
		
		portindex = realdest.find(':')  # find if there is a port
		if(portindex == -1):  
			if(pathindex == -1): # no port no path
				dest = realdest 
			else: # no port has path
				dest = realdest[:pathindex]
			port = '443' # since no port, set port as default 80
		else:
			dest = realdest[:portindex]
			if(pathindex == -1): # has port no path
				port = realdest[(portindex+1):]
			else: # has port has path
				port = realdest[(portindex+1):pathindex]

		request_line1 = 'Get ' + path + ' HTTP/1.1\n'
		request_line2 = 'Host: ' + dest + ':' + port + '\r\n'
		request = request_line1 + request_line2

		# send get request
		destsocket = socket(AF_INET, SOCK_STREAM)
		destsocket.connect((dest, int(port)))
		destsocket.sendall(request.encode())
		while True:
			destmessage = destsocket.recv(1048576)
			if(len(destmessage)>0):
				connectionSocket.send(destmessage)
			else:
				break

		destsocket.close()
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		# Fill in start
		connectionSocket.send('HTTP/1.0 404 Not Found\r\n'.encode())
        # Fill in end
        
		# Close the client connection socket
		# Fill in start
		connectionSocket.close()
        # Fill in end

serverSocket.close()