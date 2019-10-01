import socket
import time

IP = 'localhost'
PORT = 14666
BUFFER_SIZE = 1024
MESSAGE = None
NUM_REQ = 5

def main():
	STEP = 1
	RTT = 0
	REMOTE_TIME = 0
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, PORT))
	#print("Connected to server!")
	while STEP <= NUM_REQ+1:
		time.sleep(1)
		#print(STEP)
		(REMOTE_TIME, RTT )= sync(s, STEP, REMOTE_TIME, RTT)
		STEP += 1
	s.close()


def sync(s, STEP, REMOTE_TIME, RTT):
	if STEP > NUM_REQ:
		print("REMOTE_TIME " + str(round(REMOTE_TIME)) +"\nLOCAL_TIME " + str(round(time.time()))+"\nRTT_ESTIMATE "+ str(round(RTT)))
		return 1, 1
	else:
		MESSAGE = "STEP "+str(STEP) +"!"
		t0 = time.time()
		#print("sending data", MESSAGE, "At time:", t0)
		s.send(MESSAGE.encode())
		data = None
		while True:
			data = s.recv(BUFFER_SIZE)
			if data is not None and data != ' ' and data != b'':
				break 
		#print("recieved data from server:", data)
		if data is not None:
			t3 = time.time()
			#print(data, t3)
			split = data.decode().split(' ')
			t1 = float(split[3])
			t2 = float(split[5])
			RTT = (t3 - t0) - (t2 - t1)
			OFFSET = ((t1 - t0) + (t2 - t3))/2
			#print("RTT is :" + str(RTT) + " and OFFSET is " + str(OFFSET))
			return (time.time() + OFFSET, RTT)
		return 1

if __name__ == "__main__":
	main()
