import socket

data = [['import sys\n',
 'from random import randrange\n',
 '\n',
 '# generates X random numbers between 1 and 10\n',
 '# and returns the sum\n',
 'def main():\n',
 '\tx = int(sys.argv[1])\n',
 '\tsum = 0\n',
 '\tfor i in range(0,x):\n',
 '\t\tsum = sum + randrange(1,10)\n',
 '\treturn sum\n',
 '\t\n',
 "if __name__ == '__main__':\n",
 '\tprint main()'], 
	200]
	
if __name__ == '__main__':
	data1 = 'WORK,'
	for line in data[0]:
		data1 = data1+line
	data1 = data1+",{}".format('200')
	print data1
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect(("127.0.0.1", 5005))
	s.send(data1)
	
