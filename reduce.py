# takes all the results and 
# returns their sum
#!/usr/bin/env python
import sys
import traceback

def main():
	with open("error.log","w") as log:
		try:
			return_value = 0
			for result in sys.argv[1:][0].split(" "):
				return_value = return_value + int(result)
			return return_value
		except Exception, err:
			log.write("{}\n{}".format(str(traceback.format_exc()), str(sys.exc_info()[0])))
		
if __name__ == '__main__':
	print main()
