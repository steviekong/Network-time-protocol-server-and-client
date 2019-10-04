import socket
import time
import sys

IP = '0.0.0.0'
PORT = 14666
BUFFER_SIZE = 1024
MESSAGE = None
NUM_REQ = 8 # This defines the number of requests made to the NTP server

if len(sys.argv) is 2:
	IP = sys.argv[1]

def main():
	STEP = 1
	offset_array = [] # Stores the list of offsets 
	rtt_array = [] # Store the list of rtt

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, PORT))

	while STEP < NUM_REQ+1: # Loop for requests 
		time.sleep(1) # Sleep the thread before making another request
		(OFFSET, RTT)= sync(s, STEP)
		offset_array.append(OFFSET)
		rtt_array.append(RTT)
		STEP += 1
	s.close()
	min_rtt = min(rtt_array)
	min_offset = offset_array[rtt_array.index(min_rtt)]
	#print(offset_array)
	#print(rtt_array)
	print("REMOTE_TIME " + str(int((time.time() + min_offset))) + "\n" + "LOCAL_TIME " + str(int(time.time())) + "\n" + "RTT_ESTIMATE " + str(int(min_rtt)))



'''
This function requests the time from the NTP server and returns the new REMOTE TIME and RTT to the main function
'''
def sync(s, STEP):
		MESSAGE = "STEP "+str(STEP) +"!"
		t1 = time.time()
		# Sending requests to the server with the step
		s.send(MESSAGE.encode())
		data = None
		while True:
			data = s.recv(BUFFER_SIZE)
			if data is not None and data != ' ' and data != b'':
				break 
		#print("recieved data from server:", data)
		if data is not None:
			t4 = time.time()
			#print(data, t3)
			split = data.decode().split(' ')
			t2 = float(split[3])
			t3 = float(split[5])
			RTT = ((t4 - t1) - (t3 - t2))/2
			OFFSET = ((t2 - t1) + (t3 - t4))/2
			#print("RTT is :" + str(RTT) + " and OFFSET is " + str(OFFSET))
			return (OFFSET, RTT)
		
if __name__ == "__main__":
	main()
