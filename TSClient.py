import socket
import time
import sys

IP = "0.0.0.0"
PORT = 14666
BUFFER_SIZE = 1024
MESSAGE = None
NUM_REQ = 10 # This defines the number of requests made to the NTP server

if len(sys.argv) is 2:
	IP = sys.argv[1]

def main():
	STEP = 1
	RTT = 0 
	REMOTE_TIME = time.time() #Initialized as current system time. Only changes after a request is made to the NTP server 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, PORT))
	while STEP <= NUM_REQ+1: # Loop for requests 
		time.sleep(0.01) # Sleep the thread before making another request
		(REMOTE_TIME, RTT)= sync(s, STEP, REMOTE_TIME, RTT) # Updating REMOTE TIME and RTT
		STEP += 1
	s.close()


'''
This function requests the time from the NTP server and returns the new REMOTE TIME and RTT to the main function
'''
def sync(s, STEP, REMOTE_TIME, RTT):
	if STEP > NUM_REQ:
		print("REMOTE_TIME " + str(int(REMOTE_TIME)) +"\nLOCAL_TIME " + str(int(time.time()))+"\nRTT_ESTIMATE "+ str(int(RTT)))
		return 1, 1
	else:
		MESSAGE = "STEP "+str(STEP) +"!"
		t0 = REMOTE_TIME
		# Sending requests to the server with the step
		s.send(MESSAGE.encode())
		data = None
		while True:
			data = s.recv(BUFFER_SIZE)
			if data is not None and data != ' ' and data != b'':
				break 
		#print("recieved data from server:", data)
		if data is not None:
			t3 = REMOTE_TIME + (time.time() - t0)
			#print(data, t3)
			split = data.decode().split(' ')
			t1 = float(split[3])
			t2 = float(split[5])
			RTT = (t3 - t0) - (t2 - t1)
			OFFSET = ((t1 - t0) + (t2 - t3))/2
			#print("RTT is :" + str(RTT) + " and OFFSET is " + str(OFFSET))
			if REMOTE_TIME > t2 + OFFSET: # Check for if our time is faster or slower than the NTP server
				return (t2 + OFFSET + RTT, RTT)
			else:
				return (t2 - OFFSET + RTT, RTT)
		
	
		return 1, 1, 1	

if __name__ == "__main__":
	main()
