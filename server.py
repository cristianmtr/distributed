#!/usr/bin/env python

import socket

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024  

WORKERS = []

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
		print "\tReceived data:", data
		type = data.split(',')[0]
		if type == 'JOIN':
			# expecting form "JOIN,<MY_PORT>"
			if handle_join(data.split(',')[1:]) == 0:
				conn.send('0')
			else:
				conn.send('1')
		conn.close()	

if __name__ == '__main__':
	main()
	