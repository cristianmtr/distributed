# map and reduce py file should contain two comment lines at 
# very beginning describing what they do, followed by:
#!/usr/bin/env python

from random import randint
import sys
import subprocess
import socket
import random
import string

# SERVER
# By default the ip is localhost
SIGEND = '\nSIGEND'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
# WORKER
WORKER_PORT = ''
BUFFER_SIZE = 1024
# COUNTER FOR RECEIVED TASKS
TASK_ID = 0
# ID OF THE WORKER
WORKER_ID = "".join([random.choice(string.letters) for i in xrange(0,4)])

def read_socket():
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       s.bind(("",WORKER_PORT))
       print "listening on {}".format(WORKER_PORT)
       while True:
               buffer = ''
               data = True
               s.listen(0)
               conn, addr = s.accept()
               print "accepted connection"
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
                             return buffer
                      else:
                             buffer += data
                        
def work_work(data):
	global TASK_ID
	global WORKER_ID
	arg = data.split(',')[0]
	if type(arg) == list:
		arg = " ".join(arg)
	task = data[len(arg)+1:]
	with open("task_{}_{}.py".format(WORKER_ID, TASK_ID),"w") as t:
		for line in task:
			t.write(line)
	result = subprocess.check_output(["python","task_{}_{}.py".format(WORKER_ID, TASK_ID),arg])
	print "\tresult = {}".format(result)[:-1]
	return result
			
def listen_for_tasks():
	global TASK_ID
        global WORKER_PORT
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print "\tWaiting for tasks on {}".format(WORKER_PORT)
	s.bind(("",WORKER_PORT))
	while True:
		s.listen(1)
		conn, addr = s.accept()
		data = conn.recv(BUFFER_SIZE)
		if not data: 
			conn.close()		
		print "\tWORK: {}".format(data[data.find("#"):data.rfind("#")][:-1])
		TASK_ID += 1
		result = work_work(data)
		conn.send(str(result))
		conn.close()	
	return 0
	
def join_workers():
        global WORKER_PORT
        # create socket, detect own port, contact server, send JOIN request, listen for confirmation
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print 'contacting server on {}'.format(SERVER_IP, SERVER_PORT)
	s.connect((SERVER_IP, SERVER_PORT))
        ip_port = str(s.getsockname()[0]) + ',' + str(s.getsockname()[1])
        WORKER_PORT = int(s.getsockname()[1])
        print "My ip and port: {}".format(ip_port)
	JOIN_REQUEST = 'JOIN,{}{}'.format(ip_port,SIGEND)
	print "\tSending JOIN request to {}".format(SERVER_IP)
        print "\tRequest was: {}".format(JOIN_REQUEST)
	s.send(JOIN_REQUEST)
        s.close()
        message = read_socket()
        if message == '0':
                return 0
        return 1

def main():
        global SERVER_IP
	#check for server IP parameter
	#by default it is 'localhost'
	if len(sys.argv) > 1 and sys.argv[1] != "":
		SERVER_IP = sys.argv[1]	
	joined = join_workers()
	if joined == 0:
		print '\tJoined successfully'
		# listen for task
		listen_for_tasks()
	else:
		print '\tSomething went wrong'
	
if __name__ == "__main__":
	main()
