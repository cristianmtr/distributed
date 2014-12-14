# map and reduce py file should contain two comment lines at 
# very beginning describing what they do, followed by:
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
	len_map = int(data.split(',')[0])
	len_reducer = int(data.split(',')[1])
	argument = int(data.split(',')[2])
	# print argument, len_map, len_reducer
	data = data.split('{},'.format(argument))[1]
	map_task = data[:len_map]
	print "\t\tMap task: {}".format(map_task[map_task.find("#"): map_task.rfind("#")][:-1])
	reducer_task = data[len_map:len_map+len_reducer]
	print "\t\tReducer task: {}".format(reducer_task[reducer_task.find("#"): reducer_task.rfind("#")][:-1])
	arguments = [argument / len(WORKERS)]*len(WORKERS)
	for i in range(0,argument%len(WORKERS)):
		arguments[i] += 1
	pool = Pool(processes=len(WORKERS))
	results = pool.map(assign_work_and_listen_star, itertools.izip(WORKERS, arguments, itertools.repeat(map_task)))
	if len(results) > 1:
		results = [str(int(result)) for result in results]
		results = assign_work_and_listen(WORKERS[0], " ".join(results), reducer_task)	
	print "\t\tResult = {}".format("".join(results)[:-1])
	return "".join(results)

def handle_join(worker_ip_port):
	worker_ip_port = tuple(worker_ip_port)
	if worker_ip_port not in WORKERS:
		WORKERS.append(worker_ip_port)
		print '\t\tNew worker added on {}'.format(worker_ip_port)
		print '\t\tWORKERS: {}'.format(WORKERS)
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
			print "\tGot a JOIN request. Processing..."
			if handle_join(data.split(',')[1:]) == 0:
				conn.send('0')
			else:
				conn.send('1')
		elif type == 'WORK':
			# the work handler function takes
			# as parameters the code to be run
			print "\tGot a WORK request. Processing..."
			res = handle_work(data[5:])
			conn.send(res)
		conn.close()	

if __name__ == '__main__':
	main()
	
