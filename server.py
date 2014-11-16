#!/usr/bin/env python

import socket

TCP_IP = '192.168.0.100'
TCP_PORT = 5005
BUFFER_SIZE = 1024  

WORKERS = []

def handle_join(worker_ip):
	if worker_ip not in WORKERS:
		WORKERS.append(worker_ip)
		print '\t\tNew worker added on ip {}'.format(worker_ip)
		print '\t\t{}'.format(WORKERS)
		return 0
	print '\t\tThat ip is already in the worker list'
	return 1
		
# the listen forever loop
def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
			if handle_join(data.split(',')[1]) == 0:
				conn.send('0')
			else:
				conn.send('1')
		conn.close()	

if __name__ == '__main__':
	main()
	