# map and reduce py file should contain two comment lines at 
# very beginning describing what they do, followed by:
#!/usr/bin/env python

import sys
import itertools
import socket
import subprocess
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
	# data = (length of map .py file),(length of reduce .py file),(argument for map),(code for map)(code for reduce)
	# 
	# for sample of data, look at the bottom of this file
	len_map = int(data.split(',')[0])
	len_mapinput = int(data.split(',')[1])
	len_distributor = int((data.split(',')[2]))
	len_reducer = int(data.split(',')[3])
	#print len_map, len_mapinput, len_distributor, len_reducer
	data = data.split('{},'.format(len_reducer))[1]
	map_task = data[:len_map]
	#print "\t\tMap task: {}".format(map_task[map_task.find("#"): map_task.rfind("#")][:-1])
	map_input = data[len_map:len_map+len_mapinput]
	#print "\t\tMap input: {}".format(map_input)
	distributor_task = data[len_map+len_mapinput:len_map+len_mapinput+len_distributor]
	#print "\t\tDistributor task: {}".format(distributor_task[distributor_task.find("#"): distributor_task.rfind("#")][:-1])
	reducer_task = data[len_map+len_mapinput+len_distributor:len_map+len_mapinput+len_distributor+len_reducer]
	#print "\t\tReducer task: {}".format(reducer_task[reducer_task.find("#"): reducer_task.rfind("#")][:-1])
	#This WILL be passed from the requester.py
	#and will return a list of arguments for each worker
	arguments = subprocess.check_output(["python","distributor.py",str(len(WORKERS)),map_input])
	#print "arguments = {}".format(arguments)
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
			print data[5:]
			res = handle_work(data[5:])
			conn.send(res)
		conn.close()	

if __name__ == '__main__':
	main()
	
#323,441,200,# generates X random numbers between 1 and 10
## and returns the sum
##!/usr/bin/env python
#import sys
#from random import randrange
#
#def main():
#	x = int(sys.argv[1])
#	return_value = 0
#	i = 0
#	while i<x:
#		i += 1
#		return_value = return_value + randrange(1,10)
#	return return_value
#	
#if __name__ == '__main__':
#	print main()
## takes all the results and 
## returns their sum
##!/usr/bin/env python
#import sys
#import traceback
#
#def main():
#	with open("error.log","w") as log:
#		try:
#			return_value = 0
#			for result in sys.argv[1:][0].split(" "):
#				return_value = return_value + int(result)
#			return return_value
#		except Exception, err:
#			log.write("{}\n{}".format(str(traceback.format_exc()), str(sys.exc_info()[0])))
#		
#if __name__ == '__main__':
#	print main()

