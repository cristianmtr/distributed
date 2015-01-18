#distributor for sum_of_x_rand_nrs
#each worker should generate x/len(workers)+remainders rand nrs
#
import sys
import traceback

def main():
    with open("distributor_error.log","w") as log:
        try:
            args = []
            nr_workers = int(sys.argv[1])
            map_input = int(''.join(sys.argv[2:]))
            args = [map_input / nr_workers]*nr_workers
            for i in range(0,map_input%nr_workers):
                args[i] += 1
            log.write("args = \n{}".format(args))
            buffer = ''
            for arg in args:
                buffer += "{}\nSIGEND".format(arg)
            print buffer
            return 0
        except Exception, err:
            log.write("{}\n{}".format(str(traceback.format_exc()), str(sys.exc_info()[0])))
            return 1
 
    
if __name__ == '__main__':
    main()
