# map and reduce py file should contain two comment lines at 
# very beginning describing what they do, followed by:
#!/usr/bin/env python

import sys
import subprocess
import socket
import random
import string

# SERVER
# By default the ip is localhost
SERVER_IP = 'localhost'
SERVER_PORT = 5005
# WORKER
ip_port = ''
BUFFER_SIZE = 1024
# COUNTER FOR RECEIVED TASKS
TASK_ID = 0
# ID OF THE WORKER
WORKER_ID = "".join([random.choice(string.letters) for i in xrange(0,4)])

def work_work(data):
	global TASK_ID
	global WORKER_ID
	arg = data.split(',')[0]
	if type(arg) == list:
		arg = " ".join(arg)
	task = data[len(arg)+1:]
	with open("task_{}_{}.py".format(WORKER_ID, TASK_ID),"w") as t:
		for line in task:
			t.write(line)
	result = subprocess.check_output(["python","task_{}_{}.py".format(WORKER_ID, TASK_ID),arg])
	print "\tresult = {}".format(result)[:-1]
	return result
			
def listen_for_tasks(port):
	global TASK_ID
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print "\tListening on {}".format(port)
	s.bind(("",port))
	while True:
		s.listen(1)
		conn, addr = s.accept()
		data = conn.recv(BUFFER_SIZE)
		if not data: 
			conn.close()		
		print "\tWORK: {}".format(data[data.find("#"):data.rfind("#")][:-1])
		TASK_ID += 1
		result = work_work(data)
		conn.send(str(result))
		conn.close()	
	return 0
	
# notify SERVER of what port you are listening on
def join_workers(ip_port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((SERVER_IP, SERVER_PORT))
	# ex: 'JOIN,192.168.0.101,20000'
	JOIN_REQUEST = 'JOIN,{}'.format(ip_port)
	print "\tSending JOIN request to {}".format(SERVER_IP)
	s.send(JOIN_REQUEST)
	message = s.recv(BUFFER_SIZE)
	s.shutdown(socket.SHUT_RDWR) 
	s.close()
	if message == '0':
		return 0
	return 1

def main():
	global SERVER_IP
	#check for server IP parameter
	#by default it is 'localhost'
	if len(sys.argv) > 1 and sys.argv[1] != "":
		SERVER_IP = sys.argv[1]	
	# bind socket and get port number
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("",0))
	s.connect((SERVER_IP, SERVER_PORT))
	ip_port = str(s.getsockname()[0]) + ',' + str(s.getsockname()[1])
	s.shutdown(socket.SHUT_RDWR) 
	s.close()
	#print 'port inside main in {}'.format(ip_port)
	# check to see if you can join the pool of workers
	joined = join_workers(ip_port)
	if joined == 0:
		print '\tJoined successfully'
		# listen for task
		listen_for_tasks(int(ip_port.split(',')[1]))
	# else notify of something gone wrong		
	else:
		print '\tSomething went wrong'
	
if __name__ == "__main__":
	main()
