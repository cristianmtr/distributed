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
		print '''Usage: requester.py <file with map func>.py <parameter to be passed to map func> <file with reduce func>.py
example: requester.py map.py 200 reduce.py'''
		return
	try:
		maptext = ''
		mapinput = ''
		reducetext = ''
		with open(sys.argv[1], 'r') as f:
			for line in f:
				maptext += line
		if os.path.isfile(sys.argv[2]):
			with open(sys.argv[2], 'r') as f:
				for line in f:
					mapinput += line
		else:
			mapinput = sys.argv[2]
		with open(sys.argv[3],'r') as f:
			for line in f:
				reducetext += line
		lmap = len(maptext)
		lmapinput = len(mapinput)
		lreduce = len(reducetext)
		data = "WORK,{},{},{},{}{}{}".format(lmap,lmapinput,lreduce,maptext,mapinput,reducetext)
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


