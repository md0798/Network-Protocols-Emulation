import socket, pickle
import sys
import time

class Neighbor_Table():
	def __init__(self):
		self.neighbors = [] #Initialise neighbors list to send tables only to neighbors
		self.distance = [] #distance to neighbors

	def append_to(self,value,marker):
		if marker == 'n':
			self.neighbors.append(value) #append to neighbors list
		elif marker == 'd':
			self.distance.append(value) # append distance to neighbor
		else:
			return None

class Routing_Table():
	def __init__(self):
		self.local_port = None #local port
		self.destination = [] # destination list
		self.nexthop = []
		self.distance = []

	def set_local_port(self,local_port):
		self.local_port = local_port

	def append_to(self,value,marker):
		if marker == 'd':
			self.destination.append(value)
		elif marker == 'nh':
			self.nexthop.append(value)
		elif marker == 'dis':
			self.distance.append(value)
		else:
			return None


def dv():
	while True:
		data, addr = s.recvfrom(2048) # receive data
		data = pickle.loads(data) # load received data
		print("Routing table received from "+ str(addr[1]))
		if mode['setup'] == False: # for nodes without last
			mode['setup'] = True #make it true and broadcast to all neighbors 
			for y in neighbor.neighbors:
				s.sendto(pickle.dumps(routing),('',y))
				print("Message sent to " + str(y))
		
		n_index = neighbor.neighbors.index(data.local_port)#getting index of the node which sent the routing table in the neighbor table
		update = False #check if routing table is to be updated or not
		for destination in data.destination:  
			if destination != routing.local_port: 
				destination_index = data.destination.index(destination)
				if destination not in routing.destination:
					update = True #making true as new entry added
					routing.append_to(destination,'d') #adding destination to routing table
					routing.append_to(data.local_port,'nh')
					routing.append_to(neighbor.distance[n_index]+data.distance[destination_index],'dis')
				else:
					routing_table_index = routing.destination.index(destination)# getting index from routing table
					if (neighbor.distance[n_index] + data.distance[destination_index]) < routing.distance[routing_table_index]:#Checking if any shorter path to destination
						routing.distance[routing_table_index] = neighbor.distance[n_index] + data.distance[destination_index] # if true then change in routing table
						routing.nexthop[routing_table_index] = data.local_port # change nexthop
						update = True #update true as routing table changed 
		
		if update == True:
			mode['start'] = True #send routing table again as it is updated
			print('['+str(time.time())+'] Node '+str(routing.local_port)+' Routing Table')
			for i in range(len(routing.destination)): #printing the routing table
				if routing.nexthop[i]:
					print('- ('+str(routing.distance[i])+') -> Node '+str(routing.destination[i])+'; Next hop -> Node '+str(routing.nexthop[i]))
				else:
					print('- ('+str(routing.distance[i])+') -> Node '+str(routing.destination[i]))
		else: #final routing table print
			print('['+str(time.time())+'] Node '+str(routing.local_port)+' Routing Table')
			for i in range(len(routing.destination)):
				if routing.nexthop[i]:
					print('- ('+str(routing.distance[i])+') -> Node '+str(routing.destination[i])+'; Next hop -> Node '+str(routing.nexthop[i]))
				else:
					print('- ('+str(routing.distance[i])+') -> Node '+str(routing.destination[i]))

		if mode['start']: #if start mode than broadcast to neighbors
			mode['start'] = False
			for y in neighbor.neighbors:
				s.sendto(pickle.dumps(routing),('',y))
				print("Message sent to " + str(y))
		


if __name__ == '__main__':

	mode = {'start':False,'setup':False} # start used to detect last, setup if not last 
	neighbor = Neighbor_Table()
	routing = Routing_Table()
	input_info = sys.argv # getting all the values from command line
	local_port = None
	neighbor_list = []
	prob = []	
	local_port = int(sys.argv[1]) #taking variables from command line
	routing.set_local_port(local_port)
	for i in range(2,len(input_info)):
		if input_info[i] == 'last': #detect last and set mode to start
			mode['start'] = True
		elif i%2 == 0: #All the even values are neighbors 
			neighbor_list.append(int(input_info[i]))
		elif i%2 == 1: # All odd values are distance to neighbor
			prob.append(float(input_info[i]))
	
	for i in range(len(neighbor_list)): # appending value to routing table and neighbor table
		neighbor.append_to(neighbor_list[i],'n')
		routing.append_to(neighbor_list[i],'d')
		routing.append_to(None,'nh')
		
	for j in range(len(prob)):
		routing.append_to(prob[j],'dis')
		neighbor.append_to(prob[j],'d')

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',routing.local_port))
	if mode['start']: #if last detected then start broadcasting
		for y in neighbor.neighbors:
			s.sendto(pickle.dumps(routing),('',y)) #using pickle to send routing table object
			print("Message sent to " + str(y))
		mode['start'] = False 
		mode['setup'] = True
	dv() # call dv function

	while True:
		if KeyboardInterrupt:
			sys.exit()
