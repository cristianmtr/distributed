#!/usr/bin/env python

import socket
from multiprocessing import Pool

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024  

WORKERS = []

data = ''

# data should be the contents of a .py file to be run on the workers
# and the variable that can be split across the workers
# ex : ['content of calculate_sum_of_x_random_numbers.py','x = 999']

def assign_work_and_listen(worker_ip_port):
	global data
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((worker_ip_port[0], worker_ip_port[1]))
	s.send(data) 
	message = s.recv(BUFFER_SIZE)
	print message
	
def handle_work(data):
	global data
	print data
	print 
	print type(data)
	x = data.split(',')[len(data.split(','))-1]
	task = data[:len(data)-len(x)-1]
	pool = Pool(processes=len(WORKERS))
	args = 
	for i in range(0,data[1]%len(WORKERS)):
		args[i] += 1
	results = pool.map(assign_work_and_listen, (WORKERS))
		
def handle_join(worker_ip_port):
	worker_ip_port = tuple(worker_ip_port)
	if worker_ip_port not in WORKERS:
		WORKERS.append(worker_ip_port)
		print '\t\tNew worker added on port {}'.format(worker_ip_port)
		print '\t\t{}'.format(WORKERS)
		return 0
	print '\t\tThat port is already in the worker list'
	return 1
		
# the listen forever loop
# bind and listen
# distribute requests by type
# to their specific functions
def main():
	global data
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((TCP_IP, TCP_PORT))
	
	while True:
		s.listen(1)
		conn, addr = s.accept()
		data = conn.recv(BUFFER_SIZE)
		if not data: 
			conn.close()		
		# print "\tReceived data:", data[1][:5]
		print data
		print
		print
		print
		type = data.split(',')[0]
		if type == 'JOIN':
			# expecting form "JOIN,<MY_PORT>"
			if handle_join(data.split(',')[1:]) == 0:
				conn.send('0')
			else:
				conn.send('1')
		elif type == 'WORK':
			# the work handler function takes
			# as parameters the code to be run
			handle_work(data[5:])
		conn.close()	

if __name__ == '__main__':
	main()
	