# generates X random numbers between 1 and 10
# and returns the sum
#!/usr/bin/env python
import sys
from random import randrange

def main():
	x = int(sys.argv[1])
	return_value = 0
	i = 0
	while i<x:
		i += 1
		return_value = return_value + randrange(1,10)
	return return_value
	
if __name__ == '__main__':
	print main()
