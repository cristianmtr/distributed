# map and reduce py file should contain two comment lines at 
# very beginning describing what they do, followed by:
#!/usr/bin/env python

import itertools
import socket
import subprocess
from os.path import join as pathjoin
from multiprocessing import Pool, Process, Queue

TCP_IP = 'localhost'
TCP_PORT = 5005
SIGEND = "\nSIGEND"
ARGEND = "\ARGEND"
BUFFER_SIZE = 1024  

WORKERS = []

def queuer(queue):
        #
        # Listens for tasks and adds them to the queue;
        #
        while True:
                task = read_socket()
                queue.put(task)
        
def listener(queue):
        #
        # checks if the queue contains a task
        # if it does, it checks for the type 
        # and then passes it to the handler
        # 
        while True:
                if not queue.empty():
                        q_tuple = queue.get()
                        # the q_tuple will contain the data itself and the ip_port tuple of the sending host (either a worker or a requester)
                        # we will only care for that in the event of a work request
                        # so it's not used in the handle_join function
                        print "LISTENER got task"
                        type = q_tuple[0].split(",")[0]
                        if type == 'JOIN':
                                print "JOIN request processing..."
                                if handle_join(q_tuple[0].split(',')[1:]) == 1:
                                        print "Something went wrong when adding a new worker"
                        elif type == 'WORK':
                                print "Got a WORK request. Processing..."
                                data = q_tuple[0][q_tuple[0].find(',')+1:]
                                ip_port_requester = q_tuple[1]
                                results =  handle_work(data)
                                send_result_to_requester(results, ip_port_requester)
                
                
def assign_work_and_listen_star(a_b_c):
	return assign_work_and_listen(*a_b_c)

def assign_work_and_listen(worker_ip_port, arg, task):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.connect((worker_ip_port[0], int(worker_ip_port[1])))
                # print "Sent:\n{}".format(str(arg)+','+task)
		s.send(str(arg)+ARGEND+task+SIGEND) 
		message = s.recv(BUFFER_SIZE)
		return message[:-1]
	except Exception as e:
		return e

def read_socket():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("",5005))
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
                        
def handle_work(data):
	# data = "WORK,{},{},{},{},{}{}{}{}".format(lmap,lmap_input,ldistributor,lreduce,map_task,map_input,distributor_task,reduce_task)
	#
        len_map = int(data.split(',')[0])
	len_mapinput = int(data.split(',')[1])
	len_distributor = int((data.split(',')[2]))
	len_reducer = int(data.split(',')[3])
        data = data.split('{},'.format(len_reducer))[1]
	map_task = data[:len_map]
        print "map task is \n{}".format(map_task)
        map_input = data[len_map:len_map+len_mapinput]
        print "map input is \n{}".format(map_input)
        distributor_task = data[len_map+len_mapinput:len_map+len_mapinput+len_distributor]
        print "distributor task is \n{}".format(distributor_task)
        reducer_task = data[len_map+len_mapinput+len_distributor:len_map+len_mapinput+len_distributor+len_reducer]
        print "Reducer task is \n{}".format(reducer_task)
        arguments = get_arguments(distributor_task, map_input)
        print "\targuments = {}".format(arguments)
        results = get_map_results(map_task, arguments)
        print "\tresults from map: {}".format(results)
	if len(results) > 1:
		# results = [str(int(result)) for result in results]
		results = assign_work_and_listen(WORKERS[0], "".join(res for res in results), reducer_task)
        results = "".join(results)[:-1]
	print "\tResult = {}".format(results)
        return results
        
        
def get_map_results(map_task, arguments):
        global WORKERS
        pool = Pool(processes=len(WORKERS))
	results = pool.map(assign_work_and_listen_star, itertools.izip(WORKERS, arguments, itertools.repeat(map_task)))
        return results

# arguments that will be passed to each of the workers
# it is a list where each item is a string that will passed to
# the worker corresponding to its index
def get_arguments(distributor_task, map_input):
        global WORKERS
        tmp_distributor_file = pathjoin(".","tmp","distributor.py")
        with open(tmp_distributor_file, "w") as t:
                for line in distributor_task:
                        t.write(line)
	arguments = subprocess.check_output(["python",tmp_distributor_file,str(len(WORKERS)),map_input])
        arguments = arguments.split("\nSIGEND")[:-1]
        return arguments

def send_result_to_requester(results, ip_port_requester):
        results = "".join(results)
        results = results.replace(";","\n")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        i = 0
        while i<3:
                try:
                        s.connect((ip_port_requester))
                        s.send(results+SIGEND)
                        s.close()
                        return True
                except Exception:
                        i+=1
                        pass
        return False

                
def handle_join(worker_ip_port):
	worker_ip_port = tuple(worker_ip_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # print "Trying to connect to {}".format(worker_ip_port)
        for i in range(3):
                try:
                        s.connect(("",int(worker_ip_port[1])))
                        if worker_ip_port not in WORKERS:
                                WORKERS.append(worker_ip_port)
                                print '\t\tNew worker added on {}'.format(worker_ip_port)
                                print '\t\tWORKERS: {}'.format(WORKERS)
                                s.send('0'+SIGEND)
                                s.close()
                                return 0
                except Exception as e:
                        pass
	print '\t\tThat port is already in the worker list'
        s.close()
	return 1

def find_nth(text, subst, n):
        # in a string of text
        # look for substring subst
        # until you have reached the nth time it appears
        # returns the last position before that
        # occurrence of subst
        i = 0
        ret = 0
        while i != n:
                ret += text.find(subst)
                text = text[ret+1:]
                i += 1
        return ret

if __name__ == '__main__':
        q = Queue()
        a = Process(target=queuer, args=(q,))
        b = Process(target=listener, args=(q,))
        a.start()
        b.start()
