#!/usr/bin/env python

import sys
import itertools
import socket
from multiprocessing import Pool

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024  

WORKERS = []

# data should be the contents of a .py file to be run on the workers
# and the variable that can be split across the workers
# ex : ['content of calculate_sum_of_x_random_numbers.py','x = 999']

def assign_work_and_listen_star(a_b_c):
	return assign_work_and_listen(*a_b_c)

def assign_work_and_listen(worker_ip_port, arg, task):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.connect((worker_ip_port[0], int(worker_ip_port[1])))
		s.send(str(arg)+','+task) 
		# return 'Sent {}'.format(str(arg)+','+task)
		message = s.recv(BUFFER_SIZE)
		return message
	except Exception as e:
		return e
	
def handle_work(data):
	# ex: data = "<python code to be run>,<command line parameter to be divided among workers>"
	# ex: data = "import sys\n x = int(sys.argv[1])\n print sum(range(0,x))\n,200"
	# x = 200
	x = data.split(',')[len(data.split(','))-1]
	task = data[:len(data)-len(x)-1]
	pool = Pool(processes=len(WORKERS))
	x = int(x) / len(WORKERS)
	# args = [67, 67, 66]
	args = [x]*len(WORKERS) 
	for i in range(0,x%len(WORKERS)):
		args[i] += 1
	# magic
	# (worker_ip_port, 67, task)
	# are passed into a wrapper function
	results = pool.map(assign_work_and_listen_star, itertools.izip(WORKERS, args, itertools.repeat(task)))
	# results will look like ["text\r\n\", "text\r\n\"]
	return "".join(results)
		
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
			res = handle_work(data[5:])
			conn.send(res)
		conn.close()	

if __name__ == '__main__':
	main()
	
