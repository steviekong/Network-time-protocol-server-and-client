import time
import socket
import threading

IP = '0.0.0.0'
PORT = 14666
BUFFER_SIZE = 1024
NUM_REQ = 8


def main():
	# Initialize the accept socket and listen on the given port
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((IP, PORT))
	print("Server started on IP " + str(IP) + " and port " + str(PORT))
	print("Waiting for client requests")

	while True:
		server.listen(100)
		clientsock, clientAddress = server.accept()
		newthread = ClientThread(clientAddress, clientsock, STEP = 1)
		newthread.start()

#Client thread object
class ClientThread(threading.Thread):
	def __init__(self,clientAddress,clientsocket, STEP):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
		self.STEP = STEP
		print ("New connection added: ", clientAddress)
	#This function is the main thread function
	def run(self):
		while self.STEP <= NUM_REQ:
			self.sync() #calls sync for every step
		print("NTP complete, closing sockets")
		self.csocket.close()
	# Sends t2 and t3 for every client request
	def sync(self):
		recieved_message = ""
		parts = None
		t1 = None
		while True:
			data = self.csocket.recv(BUFFER_SIZE)
			print("recieved data:", data)
			recieved_message += data.decode()
			if data.decode()[len(data)-1] == '!':
				parts = recieved_message.split(' ')
				print(parts)
				t2 = time.time()
				break
		MESSAGE = "STEP "+str(self.STEP)+" "+"T2 "+ str(t2) + " " + "T3 " + str(time.time())
		print("sending data", MESSAGE)
		self.csocket.send(MESSAGE.encode())
		self.STEP += 1



if __name__ == "__main__":
	main()
