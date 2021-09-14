from socket import *
import sys
import requests

# THESE LINES ARE RANDOM COMMENTS THAT ARE JUST 
# FOR ME TO LITERALLY JUST
# EDIT THIS "NON-TRIVIAL" CODE
# IN SOME WAY FOR
# TESTING TO SEE IF I CAN USE SOURCE CTRL VIA GITHUB
# STUFF, LOL, HELLO ASWE HW0!

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]')
	sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# -----------------------------------------------------------------------------------------Fill in start.
host = sys.argv[1]
port = int(sys.argv[2])

tcpSerSock.bind((host, port))
tcpSerSock.listen()
# -----------------------------------------------------------------------------------------Fill in end.

while 1:

	# Strat receiving data from the client
	print("\nReady to serve...")

	tcpCliSock, addr = tcpSerSock.accept()
	print(">> Received a connection from:", addr)

	# message = 
	# -------------------------------------------------------------------------------------Fill in start.
	timed_out = False
	fakenews = False
	raw_message = tcpCliSock.recv(2048)
	raw_message = raw_message.decode('utf-8')
	# print("message ----------", raw_message)
	if len(raw_message.split()) < 2:
		continue
	# -------------------------------------------------------------------------------------Fill in start.

	# Extract the filename from the given message
	if str(raw_message.split()[1])[0] == "/":
		message = raw_message.split()[:1][0] + " " + str(raw_message.split()[1])[1:] + " "
		message += raw_message[len(message)+1:]
	else:
		message = raw_message

	# print("message ----------", message)
	sweet = message.split()[1]
	sweet = sweet.replace("http://", "", 1)
	# print("sweet ----------", sweet)
	filename = message.split()[1].partition("/")[2]
	filename = filename.replace("http://", "", 1)
	# print("filename ----------", filename)
	hotsea = sweet
	hotsea = hotsea.partition("/")[0]
	# print("hotsea ----------", hotsea)
	fileExist = "false"
	filetouse = "/" + filename
	# print("filetouse ----------", filetouse)

	# if str(raw_message.split()[0]) == "POST":

	# 	try:

	# 		# https://www.geeksforgeeks.org/get-post-requests-using-python/
			
	# 		milk = "http://httpbin.org/post"
	# 		apik = "0000"
	# 		browniepnts = '''print("??????????????????")
	# 		ija = 893
	# 		cdd = 2
	# 		da = ija * cdd - cdd
	# 		print(str(da))
	# 		'''
	# 		mommy = {'kiki' : 'do you love me',
	# 		'this is real' : apik,
	# 		'this is me' : 'im exactly where im supposed to be now',
	# 		'gotta let the light' : browniepnts,
	# 		'shine on me' : 'this is water'}
	# 		riri = requests.post(url=milk, data=mommy)
	# 		pastabench = riri.text

	# 	except:
	# 		print(">> Failed to post")
	# elif str(raw_message.split()[0]) == "GET":
	# 	pass
	# else:
	# 	print(">> Unsupported HTTP request method")
	# 	tcpCliSock.close()
	# 	continue

	try:
		# Check whether the file exist in the cache
		if filename == "":
			glory = sweet
			glory.replace("/", "\\")
		else:
			glory = sweet.replace("/", "\\")
		# print("glry ---------- ", glory)
		f = open(glory, "rb")
		outputdata = f.readlines()
		fileExist = "true"

		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.1 200 OK\r\n\r\n".encode('utf-8', 'ignore'))
		tcpCliSock.send("Content-Type: text/html\r\n\r\n".encode('utf-8', 'ignore'))

		# ---------------------------------------------------------------------------------Fill in start.
		for line in outputdata:
			tcpCliSock.send(line)
		# ---------------------------------------------------------------------------------Fill in end.

		print(">> Request summary:", raw_message.partition("\n")[0])
		print(">> Read from cache")

	# Error handling for file not found in cache
	except IOError:

		if fileExist == "false":

			# Create a socket on the proxyserver
			# c = 
			# -----------------------------------------------------------------------------Fill in start.
			not_200 = False
			c = socket(AF_INET, SOCK_STREAM)
			# -----------------------------------------------------------------------------Fill in end.

			hostn = filename.replace("www.", "", 1)
			# print("hostn ----------", hostn)

			try:

				# Connect to the socket to port 80
				# -------------------------------------------------------------------------Fill in start.
				portn = 80
				try:
					print(hotsea)
					c.connect((hotsea, portn))
				except:
					fakenews = True
					print(">> Request summary:", raw_message.partition("\n")[0])
					print(">> Failed to connect to requested address")
					raise
				# print("*")
				# -------------------------------------------------------------------------Fill in end.

				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				getpreppy = "GET " + "http://" + sweet + "/" + " HTTP/1.1\n\n"
				# print("getpreppy ----------", getpreppy)
				c.send(getpreppy.encode('utf-8', 'ignore'))
				# print("**")
				
				# Read the response into buffer
				# -------------------------------------------------------------------------Fill in start.
				req_line = True
				wap = c.makefile("rwb", None, errors='replace')
				# print("***")
				try:
					wap_line = wap.readline()
					# print("hi here!")
					wap_line = wap_line.decode('utf-8')
					# print("wap_line:", wap_line)
				except TimeoutError:
					timed_out = True
					raise
				# print("****")
				bufdude = ""

				while wap_line != "":

					if req_line:
					
						# print("*****")
						req_line = False
						print(wap_line.split()[1])
						if "200" not in wap_line.split()[1]:
							not_200 = True
							wap.close()
							print(">> Request summary:", raw_message.partition("\n")[0])
							print(">> Response:", wap_line)
							# print("fakenews)")
							tcpCliSock.send(wap_line.encode('utf-8', 'ignore'))
							tcpCliSock.close()
							raise
						else:
							# print("******")
							bufdude += wap_line
							tcpCliSock.send(wap_line.encode('utf-8', 'ignore'))

					else:
						print("****1***")
						try:
							wap_line = wap.readline()
							# print("hi here!")
							# print("wap_line:", wap_line)						
							wap_line = wap_line.decode('utf-8', 'ignore')
							# print("****2****")
							bufdude += wap_line
							tcpCliSock.send(wap_line.encode('utf-8', 'ignore'))
						except TimeoutError:
							timed_out = True
							raise
						# print("****3*****")
				# print("\n\n***fjidsalubjkjalkd*\n\n\nHALLELUJAHHHHHAHAHAH\n\n\n")
				# -------------------------------------------------------------------------Fill in end.

				# Create a new file in the cache for the requested file
				# Also send the response in the buffer to client socket and the corresponding file in the cache
				if filename == "":
					glory = sweet.replace("/", "\\")
					print(glory, glory)
				else:
					glory = sweet.replace("/", "\\")
				print(">> Stored in cache:", glory)
				print(glory)
				tmpFile = open("./"+ glory, "ab+")
				# print("*******00000000***")

				# -------------------------------------------------------------------------Fill in start.
				tmpFile.write(bufdude.encode('utf-8', 'ignore'))
				tmpFile.close()
				wap.close()
				c.close()
				# -------------------------------------------------------------------------Fill in end.

			except:
				if not_200:
					continue
				if timed_out:
					print(">> Request summary:", raw_message.partition("\n")[0])
					print(">> TimeoutError: [Errno 60] Operation timed out")
					continue
				if fakenews:
					tcpCliSock.close()
					continue
				print(">> Illegal request")
				sys.stderr.write('%s')

		else:
				# HTTP response message for file not found
				
				# -------------------------------------------------------------------------Fill in start.
				tcpCliSock.send("HTTP/1.1 404 File Not Found\r\n\r\n".encode('utf-8', 'ignore'))
				# -------------------------------------------------------------------------Fill in end.

	# Close the client and the server sockets
	tcpCliSock.close()

# -----------------------------------------------------------------------------------------Fill in start.
tcpSerSock.close()
# -----------------------------------------------------------------------------------------Fill in end.
