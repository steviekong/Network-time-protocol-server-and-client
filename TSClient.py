import socket
import time

IP = 'localhost'
PORT = 14666
BUFFER_SIZE = 1024
MESSAGE = None
RTT = None
REMOTE_TIME = None
NUM_REQ = 5

def main():
	STEP = 1
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, PORT))
	while STEP <= NUM_REQ:
		time.sleep(1)
		print(STEP)
		sync(s, STEP)
		STEP += 1
	print("done with while loop")
	s.close()


def sync(s, STEP):
	if STEP > NUM_REQ:
		print("REMOTE_TIME " + REMOTE_TIME+"\n"+"LOCAL_TIME " + time.time()+"\n"+"RTT_ESTIMATE "+RTT)
		return
	else:
		MESSAGE = "STEP "+str(STEP) +"!"
		t1 = time.time()
		print("sending data", MESSAGE, "At time:", t1)
		s.send(MESSAGE.encode())
		data = None
		while True:
			data = s.recv(BUFFER_SIZE)
			if data is not None and data != ' ' and data != b'':
				print(data)
				break 
		print("recieved data from server:", data)
		if data is not None:
			t2 = time.time()
			print(data, t2)
			print("RTT is", (t2 - t1)/2 )
			RTT = (t2 - t1)/2
			split = data.decode().split(' ')
			REMOTE_TIME = split[3]
	return

if __name__ == "__main__":
	main()
