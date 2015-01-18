distrib
=======

Project for learning distributed systems architecture

USE CASE FOR THE TIME BEING

"python server.py"

"python worker.py" (can be started as many times as you want. it will just add more workers to the pool)

"python requester.py <arguments>" (read the help text for more info on the argumnets to be passed)

Tested on Windows and Linux. 


NOTES
=====

PROBLEMS
- The tasks for additions and multiplication need to be updated to the key-value system. Need to pay attention to formatting of results and arguments. 
- Find out why there are orphaned server processes after Keyboard Interrupt is issued

CAN BE OPTIMIZED
worker.py
arg = data.split can be replaced with something like arg = data[:data.find(ARGEND)]

