import threading
import time
import sys
import json
import socket
import random
from queue import Queue

TIMEOUT = 500 # in ms

class Window(): 
	def __init__(self, window_size):
		self.window_size = window_size # define window size
		self.start_index = 0 
		self.end_index = 0 
		self.pointer = 0 

	def move_window(self): # moving window 
		self.start_index += 1

	def increment_pointer(self): 
		self.pointer += 1

	def set_end_index(self,data_size): # end of window
		self.end_index += data_size

class Timer(): 
	def __init__(self):
		self.time = None
		self.status = False

	def start(self):
		self.time = time.time() #the current time
		self.status = True

	def stop(self):
		self.status = False

	def timeout(self):
		if self.status == True and (time.time() - self.time)*1000 > TIMEOUT: #checking for timeout
			return True
		return False


def initialize_data_buffer(message_buffer, data_buffer):
	while True:
		print("node>", end = " ") #displayed first 
		data = input()
		if data[:5] == "send ":
			message = data[5:] #getting message
			message_buffer.put(message) 
			window.set_end_index(len(message)) # end index is message length

			for i in range(len(message)):
				seq_num = window.end_index - len(message) + i
				data = message[i] 
				data_buffer[window.end_index - len(message) + i] = {'seq': seq_num, 'data': data, 'ack':False} # making data buffer with seq,data and ack
		else:
			print("Invalid input!!")
			continue


def discard_packet(last_seq_num, packet, drop_packet): #discard packet function
	if drop_packet["method"]=="-d": # deterministic approach
		if last_seq_num % drop_packet['value'] == 0: #multiple of value is dropped
			if packet['ack'] == False:# check if packet is ack or data
				print("["+str(round(time.time(),3))+"] packet"+str(packet['seq']) + " " + str(packet['data'])+" discarded")
			elif packet['ack'] == True:
				print("["+str(round(time.time(),3))+"] ACK"+str(packet['seq'])+" discarded")
			return True #if dropped
		else:
			return False
	if drop_packet["method"] == '-p': # probablistic approach
		if random.random() <= drop_packet['value']:#random gives value between 0 and 1
			if packet['ack'] == False:# check if packet is ack or data
				print("["+str(round(time.time(),3))+"] packet"+str(packet['seq'])+ " "+ str(packet['data']) +" discarded")
			elif packet['ack'] == True:
				print("["+str(round(time.time(),3))+"] ACK" + str(packet['seq']) +" discarded")
			return True
		else:
			return False

def send(receiver_port, timer, window, drop_packet, data_buffer, ack_list): #send function
	while True:
		if timer.timeout() == True:# check for timeout
			print("["+str(round(time.time(),3))+"] packet"+str(window.start_index)+" timeout")
			for i in range(window.start_index, window.pointer):
				packet = data_buffer[i]#if timeout send all the packets again from the timed out packet
				s.sendto(json.dumps(packet).encode(), ('',receiver_port))
				if packet['ack']==False: # check if packet is ack or data
					print("["+str(round(time.time(),3))+"] packet"+str(packet['seq'])+ " " +str(packet['data'])+" sent")
				if packet['ack']==True:
					print("["+str(round(time.time(),3))+"] ACK"+str(packet['seq'])+" sent, expecting packet "+ str(packet['seq'] + 1))
			timer.start()#start timer again
		if window.pointer < window.start_index + window.window_size:#check where pointer is within window
			if data_buffer[window.pointer] != None:
				packet = data_buffer[window.pointer]#send packet at pointer
				s.sendto(json.dumps(packet).encode(), ('',receiver_port))
				if packet['ack']==False:#check if packet is ack or data
					print("["+str(round(time.time(),3))+"] packet"+str(packet['seq'])+ str(packet['data'])+" sent")
				if packet['ack']==True:
					print("["+str(round(time.time(),3))+"] ACK"+str(packet['seq'])+" sent, expecting packet "+ str(packet['seq'] + 1))
				window.increment_pointer()
				timer.start()


def receive(sender_port, timer, window, drop_packet, data_buffer, received_seq_list):
	packets_dropped = 0
	last_seq_num = 0
	while True:
		data, addr = s.recvfrom(1024) 
		packet = json.loads(data.decode("utf-8"))#receive data
		if packet['ack']==False and packet['seq'] == -2: #all packets sent
			print("[Summary] " + str(packets_dropped)+"/"+str(last_seq_num)+" packets dropped, loss rate = "+str(round((packets_dropped/last_seq_num)*100,3))+"%")
			print('node>', end = " ")#start again
			sys.stdout.flush()
			timer.stop()
		else:
			last_seq_num += 1 #increment pointer
			if not discard_packet(last_seq_num,packet,drop_packet): #checking is packet is discarded 
				if packet['ack'] == False and packet['seq'] != -2:#received data packet
					print("["+str(round(time.time(),3))+"] packet"+str(packet['seq'])+ str(packet['data'])+" received")

					if packet['seq'] == 0 or received_seq_list[packet['seq']-1] == True:#if right packet send ack
						ack_packet = {'seq':packet['seq'],'data':None,'ack':True}
						received_seq_list[packet['seq']] = True #make latest data received

						s.sendto(json.dumps(ack_packet).encode(), ('',sender_port))#send ack packet
						if ack_packet['ack']==True:
							print("["+str(round(time.time(),3))+"] ACK"+str(ack_packet['seq'])+" sent, expecting packet" + str(ack_packet['seq'] + 1))
					else:  
						for i in range(len(received_seq_list)):#updating received sequence list
							if received_seq_list[i] == False:
								last_received_seq = i-1
								break
						ack_packet = {'seq':last_received_seq,'data':None,'ack':True}#last ack
						s.sendto(json.dumps(ack_packet).encode(), ('',sender_port))
						if ack_packet['ack']==False:
							print("["+str(round(time.time(),3))+"] packet"+str(ack_packet['seq'])+" "+ str(ack_packet['data'])+" sent")
						if ack_packet['ack']==True:
							print("["+str(round(time.time(),3))+"] ACK"+str(ack_packet['seq'])+" sent, expecting packet "+str(ack_packet['seq'] + 1))

				elif packet['ack'] == True:# received an ack
					print("["+str(round(time.time(),3))+"] ACK"+str(packet['seq'])+" received, window moves to "+str(packet['seq'] + 1))

					if data_buffer[packet['seq']] == None:
						pass
					else: 
						data_buffer[packet['seq']] = None 
						window.start_index = packet['seq'] + 1

						if window.start_index != window.pointer:
							timer.start()
						else:
							timer.stop()

							if window.start_index == window.end_index:
								print("[Summary] " + str(packets_dropped)+"/"+str(last_seq_num)+" packets dropped, loss rate = "+str(round((packets_dropped/last_seq_num)*100,3))+"%")
								print('node>', end = " ")
								sys.stdout.flush()
								timer.stop()
								last_msg = {'seq':-2,'data':None,'ack':False}#last msg sent after everything is done
								s.sendto(json.dumps(last_msg).encode(),('',sender_port))		
			else:
				packets_dropped += 1 #count number of packets
			

if __name__ == '__main__':
	
	assert len(sys.argv) == 6, "The input command format should be: $ python gbnnode.py <self-port> <peer-port> <window-size> [-d <value-of-n>|-p <value-of-p>]" #checking if input is correct or not
	#Initialize all the arguments provided in command line
	self_port = int(sys.argv[1]) # defining variables
	peer_port = int(sys.argv[2])
	window_size = int(sys.argv[3])
	drop_packet = {"method": sys.argv[4], "value": float(sys.argv[5])}
	
	data_buffer = [None]*1024 # defining the data buffer 
	window = Window(window_size) #defining window size
	timer = Timer()

	ack_list = {'seq':-1, 'status':False} #dict for ack 
	received_seq_list = [False] * 2000 #list of all received packets, initally false

	#Start socket 
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',self_port))

	# Start sender process
	t1 = threading.Thread(target=send, args=(peer_port, timer, window, drop_packet, data_buffer, ack_list))
	t1.start()
	#Satrt receiver process
	t2 = threading.Thread(target=receive, args =(peer_port, timer, window, drop_packet, data_buffer, received_seq_list))
	t2.start()

	#Initialize data buffer
	message_buffer = Queue()
	t3 = threading.Thread(target=initialize_data_buffer, args=(message_buffer,data_buffer))
	t3.start()

	while True:
		if KeyboardInterrupt:
			sys.exit()


