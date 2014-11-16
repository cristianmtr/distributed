#!/usr/bin/env python

import socket

SERVER_IP = '192.168.0.100'
TCP_PORT = 5005
BUFFER_SIZE = 1024

def get_my_ip():
	# Hack. Need to develop function to discover own ip.
	# so that the code can be deployed to machines
	# and run immediately
	return '192.168.0.101'

def join_workers(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((SERVER_IP, TCP_PORT))
	JOIN_REQUEST = 'JOIN,{}'.format(ip)
	s.send(JOIN_REQUEST)
	message = s.recv(BUFFER_SIZE)
	s.close()
	if message == '0':
		return 0
	return 1

def main():
	MY_IP = get_my_ip()
	joined = join_workers(MY_IP)
	if joined == 0:
		print 'Joined successfully'
	else:
		print 'Something went wrong'
	
if __name__ == "__main__":
	main()
