import time
import socket
import threading

IP = 'localhost'
PORT = 14666
BUFFER_SIZE = 1
NUM_REQ = 5


def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((IP, PORT))
	print("Server started on IP " + str(IP) + " and port " + str(PORT))
	print("Waiting for client requests")

	while True:
		server.listen(1)
		clientsock, clientAddress = server.accept()
		newthread = ClientThread(clientAddress, clientsock, STEP = 1)
		newthread.start()

class ClientThread(threading.Thread):
	def __init__(self,clientAddress,clientsocket, STEP):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
		self.STEP = STEP
		print ("New connection added: ", clientAddress)

	def run(self):
		while self.STEP <= NUM_REQ:
			self.sync()
		print("NTP complete, closing sockets")
		self.csocket.send("complete!".encode())
		self.csocket.close()


	def sync(self):
		recieved_message = ""
		parts = None
		while True:
			data = self.csocket.recv(BUFFER_SIZE)
			print("recieved data:", data)
			recieved_message += data.decode()
			if data.decode() == '!':
				parts = recieved_message.split(' ')
				print(parts)
				break
	
		MESSAGE = "STEP "+str(self.STEP)+" "+"TIME "+ str(time.time())
		print("sending data", MESSAGE)
		self.csocket.send(MESSAGE.encode())
		self.STEP += 1



if __name__ == "__main__":
	main()
