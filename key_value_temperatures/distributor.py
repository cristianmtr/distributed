# distributor for the max_temperature task
# splits lines evenly between nr workers
# prnt will look like:
# 'Toronto, 20;Rome, 39;Rome, 35;'
import sys
import traceback
import itertools

def main():
    with open("distributor.log","w") as log:
        try:
            log.write("{}".format(sys.argv[1]))
            nr_workers = int(sys.argv[1])
            args = [""] * nr_workers
            log.write("args = {}".format(args))
            kvp = "".join(x for x in sys.argv[2:])
            kvp = kvp.split("\r\n")[:-1]
            for line in kvp:
                log.write("line: {}".format(line))
            workers_index = [i for i in range(nr_workers)]
            workers_index = itertools.cycle(workers_index)
            i = 0 # loop through the contents of the lines
            j = workers_index.next()  # loop through the workers. decide who's turn it is to get a line
            # should work as: args[j] += kvp[i] \ j = workers.next()
            while i < len(kvp):
                args[j] += kvp[i] + ";"
                j = workers_index.next()
                i += 1
            log.write("args = {}".format(args))                
            prnt = ""
            for arg in args:
                prnt += "{}\nSIGEND".format(arg)
            print prnt
            return 0 
        except Exception as e:
            log.write("{}\n{}".format(str(traceback.format_exc()), str(sys.exc_info()[0])))
            return 1
                                    
if __name__ == "__main__":
    main()

