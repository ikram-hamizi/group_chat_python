
'''____ SERVER____
- Listens and Connects to multiple clients (GROUP CHAT).
- Receives + transfers messages to multiple clients (in PARALLEL).
'''

import socket
import logging
from concurrent.futures import ThreadPoolExecutor #manages worker threads

class Server:

	HEADER_LENGTH = 10 #fixed length header = max number of chars in a message

	def __init__(self,IP,PORT):
		self.logger = self._setup_logger()
		self.server_socket = self._setup_socket(IP, PORT)
		self.sockets_list = [] 

	# returns a dictionary {"header":header, "data":data} or false
	def receive_from_client(self, clientsocket):
		try:

			header = clientsocket.recv(Server.HEADER_LENGTH)

			if not len(header): #if we didn't get any data
				return False

			text_length = int(header.decode('utf-8')) #full text length
			return {"header":header, "data":clientsocket.recv(text_length)}

		except:
			return False

	#accept messages + relay them to the other clients
	def run(self):
		self.logger.info("-- Server --")

		with ThreadPoolExecutor() as executer:
			while True:	
			
				clientsocket, address = self.server_socket.accept() #blocked on accept

				user = self.receive_from_client(clientsocket)

				if user is False: # disconnected
					self.logger.info(user)
					continue;

				self.sockets_list.append(clientsocket) #add client
				self.logger.info(f"New Connection established from username: [{user['data'].decode('utf-8')}] [{address[0]}:{address[1]}]")

				executer.submit(self.distribute_text, clientsocket, address, user, self.receive_from_client)

	def distribute_text(self, clientsocket, address, user, receive_from_client):
		while True:

			message = receive_from_client(clientsocket)
			text_username = user['data'].decode('utf-8')

			if not message:
				self.logger.info("No text received. Connection is lost.")
				sockets_list.remove(user)
				break;
			
			text = message['data'].decode('utf-8')
			

			print(f"Received message from {text_username}: {text}")
			
			print("#clients:", len(self.sockets_list))

			for client in self.sockets_list:				
				client.send(user['header']+user['data']+message['header']+message['data']) #ENCODED #DON'T FORGET TO >>>ENCODE<<<

	@staticmethod
	def _setup_socket(IP,PORT):

		# 1. Creaete a streaming socket object
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# 2. This allows to reconnect to server (avoids printing server is in use)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # we will set the 2nd arg to the 3rd arg (1=True)

		# 3. Bind the socket to a tuple (IP, PORT)
		server_socket.bind((IP, PORT)) #i.e. local host 127.0.0.1, #lower digts are occupied by other programs

		# 4. Make server listen for incoming connections
		server_socket.listen() 

		return server_socket

	@staticmethod
	def _setup_logger():
		logger = logging.getLogger('chat_server')
		logger.addHandler(logging.StreamHandler())
		logger.setLevel(logging.DEBUG)
		return logger


if __name__ == "__main__":

	# IP = "127.0.0.1" #or 'localhost' or socket.gethostname()
	# PORT = 8989

	from settings import SERVER_IP, SERVER_PORT
	
	server = Server(SERVER_IP, SERVER_PORT)
	server.run()


# Code tutorial:
# 1. https://www.youtube.com/watch?v=iXL-akeLTA4
# 2. https://www.youtube.com/watch?v=Lbfe3-v7yE0
