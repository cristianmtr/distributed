#!/usr/bin/env python
#

import socket
import sys
import traceback
import os.path

BUFFER_SIZE = 1024
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
SIGEND = "\nSIGEND"

def main():
	if len(sys.argv) <= 2:
		print '''Usage: requester.py <file with map func>.py <map input> <distributor> <file with reduce func>.py
example: requester.py map.py 200 reduce.py'''
		return
	try:
                print "argv1 = {}".format(sys.argv[1])
                print "argv2 = {}".format(sys.argv[2])
                print "argv3 = {}".format(sys.argv[3])
                print "argv4 = {}".format(sys.argv[4])
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
                # data now includes the ip and port of the requester
                # WORK,127.0.0.1,5200
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(("",6006))
		s.connect((SERVER_IP, SERVER_PORT))
                ip_port = str(s.getsockname()[0]) + ',' + str(s.getsockname()[1])
                data = "WORK,{},{},{},{},{}{}{}{}".format(lmap,lmap_input,ldistributor,lreduce,map_task,map_input,distributor_task,reduce_task)
                s.send(data+SIGEND)
		s.shutdown(socket.SHUT_RDWR)
		s.close()
                res = read_socket()[0]
		print res
	except Exception as e:
		print "{}\n{}".format(str(traceback.format_exc()), str(sys.exc_info()[0]))

def read_socket():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("",6006))
        while True:
                buffer = ''
                data = True
                s.listen(0)
                conn, addr = s.accept()
                while data:
                        data = conn.recv(BUFFER_SIZE)
                        # if the SIGNAL for end of packet is found in current packet
                        # add only up to that part
                        # close socket
                        # return data
                        if data.find(SIGEND) != -1:
                                buffer += data[:data.rfind(SIGEND)]
                                conn.close()
                                s.close()
                                return (buffer, addr)
                        else:
                                buffer += data
                                
if __name__ == '__main__':
	main()


