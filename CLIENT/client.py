'''____ CLIENT____
- Connect to server
- Sends/Recevies messages to/from server (in PARALLEL)
'''

import socket
import errno 
import sys
import logging
from threading import Thread
from datetime import datetime
import sys 

class Client:

	HEADER_LENGTH = 10 #fixed length header = max number of chars in a message

	def __init__(self, IP, PORT):
		self.logger = self._setup_logger()
		self.clientsocket = self._setup_socket(IP, PORT)
				
		self.inp_USERNAME = input("ENTER USERNAME:")
		self.USERNAME = self.inp_USERNAME.encode("utf-8")
		self.USERNAME_HEADER = f"{len(self.USERNAME):<{Client.HEADER_LENGTH}}".encode("utf-8")

		thread = Thread(target=self.send_text, args=(Client.HEADER_LENGTH, self.USERNAME))
		thread.daemon = True
		thread.start()

		# 1. send username to server
		self.clientsocket.send(self.USERNAME_HEADER + self.USERNAME)

		# 2. accept chat text from server infinitely
		while True:
			try:
				#1. get the username header
				recv_username_header = self.clientsocket.recv(Client.HEADER_LENGTH) #BUFFER SIZE = HEADER_LENGTH

				if not len(recv_username_header): #if header is empty, we didn't get any data
					pirnt("Connection closed by the server [x]")
					sys.exit()

				#2. get the username of the other client
				recv_username_length = int(recv_username_header.decode('utf-8'))
				recv_username = self.clientsocket.recv(recv_username_length).decode('utf-8')

				#3. get the text from the other client + print it
				recv_text_header = self.clientsocket.recv(Client.HEADER_LENGTH)
				recv_text_length = int(recv_text_header.decode('utf-8'))
				recv_text = self.clientsocket.recv(recv_text_length).decode('utf-8') #BUFFER SIZE = text_length

				# 4. >>>>>>>>>>>>>>>>>>PRINT RECEIVED TEXT FROM SERVER
				time = datetime.now().strftime("%d-%m-%Y, %H:%M")
				print(f"[{time}] {recv_username} > {recv_text}")
				

			# #expected errors
			except IOError as e:
				if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
					print("Reading error: ", str(e))
					sys.exit()
				continue

			except Exception as e:
				print("ERROR", str(e))
				sys.exit()


	# Send a text to server
	def send_text(self, HEADER_LENGTH, USERNAME):
		# Accept chat text infinitely
		while True:
			text = input()

			if text: #not empty
				text = text.encode('utf-8') #replace error with \n
				text_header = f"{len(text):<{HEADER_LENGTH}}".encode('utf-8')
				self.clientsocket.send(text_header + text)


	@staticmethod
	def _setup_socket(IP,PORT):
		# CLIENT SOCKET
		# 1. Creaete a streaming socket object
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# 2. instead of binding, this socket connects to IP and PORT
		clientsocket.connect((IP, PORT)) #in this case, client is also on 127.0.0.1

		# 3. unblock recv function
		#clientsocket.setblocking(False) 

		return clientsocket

	@staticmethod
	def _setup_logger():
		logger = logging.getLogger('chat_server')
		logger.addHandler(logging.StreamHandler())
		logger.setLevel(logging.DEBUG)
		return logger



if __name__ == "__main__":

	#IP = "127.0.0.1" #or 'localhost' or socket.gethostname()
	#PORT = 8989
	
	from settings import SERVER_IP, SERVER_PORT

	client = Client(SERVER_IP, SERVER_PORT)



# Code tutorial:
# 1. https://www.youtube.com/watch?v=iXL-akeLTA4
# 2. https://www.youtube.com/watch?v=Lbfe3-v7yE0
