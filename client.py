#!/usr/bin/env python

import subprocess
import socket

# SERVER
# By default the ip is localhost
SERVER_IP = 'localhost'
SERVER_PORT = 5005
# WORKER
ip_port = ''
BUFFER_SIZE = 1024

def work_work(data):
	# print 'Got data: {}'.format(data)
	arg = data.split(',')[0]
	task = data[len(arg)+1:]
	with open("task.py","w") as t:
		for line in task:
			t.write(line)
	result = subprocess.check_output(["python","task.py",arg])
	# print "arg = {}".format(arg)
	print "result = {}".format(result)
	return result
			
def listen_for_tasks(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print port
	s.bind(("",port))
	while True:
		s.listen(1)
		conn, addr = s.accept()
		data = conn.recv(BUFFER_SIZE)
		if not data: 
			conn.close()		
		print "\tReceived data:", data
		# TODO
		result = work_work(data)
		conn.send(str(result))
		conn.close()	
	return 0
	
# notify SERVER of what port you are listening on
def join_workers(ip_port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((SERVER_IP, SERVER_PORT))
	print '\tip_port inside join is {}'.format(ip_port)
	# ex: 'JOIN,192.168.0.101,20000'
	JOIN_REQUEST = 'JOIN,{}'.format(ip_port)
	s.send(JOIN_REQUEST)
	message = s.recv(BUFFER_SIZE)
	print '\tmessage is {}'.format(message)
	s.shutdown(socket.SHUT_RDWR) 
	s.close()
	if message == '0':
		return 0
	return 1

def main():
	# bind socket and get port number
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("",0))
	s.connect((SERVER_IP, SERVER_PORT))
	ip_port = str(s.getsockname()[0]) + ',' + str(s.getsockname()[1])
	print 'ip_port {} is {}'.format(type(ip_port),ip_port)
	s.shutdown(socket.SHUT_RDWR) 
	s.close()
	#print 'port inside main in {}'.format(ip_port)
	# check to see if you can join the pool of workers
	joined = join_workers(ip_port)
	if joined == 0:
		print 'Joined successfully'
		# listen for task
		print 'ip_port is {}'.format(ip_port)
		print type(ip_port)
		listen_for_tasks(int(ip_port.split(',')[1]))
	# else notify of something gone wrong		
	else:
		print 'Something went wrong'
	
if __name__ == "__main__":
	main()
