#!/usr/bin/env python
#should store map.py and reduce.py
#in a string
#with length headers for easier parsing on the 
#server side
#(len1)(len2)(map.py)(reduce.py)

import socket

BUFFER_SIZE = 1024

def main():
	maptext = ''
	reducetext = ''
	with open('map.py', 'r') as f:
		for line in f:
			maptext += line
	with open('reduce.py','r') as f:
		for line in f:
			reducetext += line
	lmap = len(maptext)
	lreduce = len(reducetext)
	data = "WORK,{},{},200,{}{}".format(lmap,lreduce,maptext,reducetext)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("",6006))
	s.connect(("127.0.0.1", 5005))
	s.send(data)
	res = s.recv(BUFFER_SIZE)
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	print res

if __name__ == '__main__':
	main()


