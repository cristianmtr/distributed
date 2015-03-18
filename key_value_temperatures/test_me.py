#!/usr/bin/python
# Tester program: checks if the server and worker are still working properly
# It tests the case found in this directory
# $ cat req_key_value_defaults.txt
# requester.py key_value_temperatures/map.py key_value_temperatures/map.input key_value_temperatures/distributor.py key_value_temperatures/reduce.py
# @args nr_of_workers : no. of workers to be spawned and added to the server's WORKERS list
from sys import argv
import os
from subprocess import Popen, PIPE
import pdb

# get nr of workers to spawn
nr_of_workers = int(argv[1])
# move cwd up to distributed/
os.chdir('..')
# get rel path to TMP dir
tmp_dir = os.path.join('.','tmp')
# initiate server
pdb.set_trace()
server_command = ['python', 'server.py']
path_server_log = os.path.join(tmp_dir,'server.log')
server_log = open(path_server_log,'w')
server_proc = Popen(server_command, stdout=server_log)
# initiate workers
worker_command = ['python', 'worker.py']
worker_procs = []
# iterate through workers
# and start them
# i = 1
# while i != nr_of_workers:
path_this_workers_log = os.path.join(tmp_dir,'worker_{}.log'.format(1))
this_workers_log = open(path_this_workers_log, 'w')
worker_proc = Popen(worker_command, stdout=this_workers_log)
# worker_procs.append(worker_proc)
# i += 1
# initiate requester with appropriate args
requester_command = ["python", "requester.py", "key_value_temperatures/map.py", "key_value_temperatures/map.input", "key_value_temperatures/distributor.py", "key_value_temperatures/reduce.py"]
requester_proc = Popen(requester_command, stdout=PIPE)
(output, err) = requester_proc.communicate()
print output
# and parse output
# check output ?
    
