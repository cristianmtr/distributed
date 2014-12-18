#!/usr/bin/env python
#

import socket
import sys
import traceback
import os.path

BUFFER_SIZE = 1024
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005

def main():
	if len(sys.argv) <= 2:
		print '''Usage: requester.py <file with map func>.py <map input> <distributor> <file with reduce func>.py
example: requester.py map.py 200 reduce.py'''
		return
	try:
		map_task = ''
		map_input = ''
		distributor_task = ''
		reduce_task = ''
		with open(sys.argv[1], 'r') as f:
			for line in f:
				map_task += line
		if os.path.isfile(sys.argv[2]):
			with open(sys.argv[2], 'r') as f:
				for line in f:
					map_input += line
		else:
			map_input = sys.argv[2]
		with open(sys.argv[3],'r') as f:
			for line in f:
				distributor_task += line
		with open(sys.argv[4],'r') as f:
			for line in f:
				reduce_task += line
		lmap = len(map_task)
		lmap_input = len(map_input)
		ldistributor = len(distributor_task)
		lreduce = len(reduce_task)
		data = "WORK,{},{},{},{},{}{}{}{}".format(lmap,lmap_input,ldistributor,lreduce,map_task,map_input,distributor_task,reduce_task)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(("",6006))
		s.connect((SERVER_IP, SERVER_PORT))
		s.send(data)
		res = s.recv(BUFFER_SIZE)
		s.shutdown(socket.SHUT_RDWR)
		s.close()
		print res
	except Exception as e:
		print "{}\n{}".format(str(traceback.format_exc()), str(sys.exc_info()[0]))

if __name__ == '__main__':
	main()


