import socket

BUFFER_SIZE = 1024

data = [['import sys\n',
 'from random import randrange\n',
 '\n',
 '# generates X random numbers between 1 and 10\n',
 '# and returns the sum\n',
 'def main():\n',
 '\tx = int(sys.argv[1])\n',
 '\tsum = 0\n',
 '\ti=0\n',
 '\twhile i<x:\n',
 '\t\ti = i+1\n',
 '\t\tsum = sum + randrange(1,10)\n',
 '\treturn sum\n',
 '\t\n',
 "if __name__ == '__main__':\n",
 '\tprint main()'], 
	9999999]
	
if __name__ == '__main__':
	data1 = 'WORK,'
	for line in data[0]:
		data1 = data1+line
	data1 = data1+",{}".format('9999')
	print data1
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("",6006))
	s.connect(("127.0.0.1", 5005))
	s.send(data1)
	res = s.recv(BUFFER_SIZE)
	s.shutdown(socket.SHUT_RDWR) 
	s.close()
	print res
