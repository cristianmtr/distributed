# DO NOT CONFUSE WITH MAP.PY
# for each key in key - value pair received
# returns the maximum of all its keys
# expecting: 'Toronto, 20;Tokyo, 25;Toronto, 14;Rome, 39;Tokyo, 21;Sydney, 29;Rome, 35;Sydney, 27;'
import sys

def main():
    kvp = ''.join(sys.argv[1:])
    kvp = kvp.split(";")[:-1]
    dc = {}
    i = 0
    while i < len(kvp):
        kvp[i] = kvp[i].split(',')
        kvp[i][1] = int(kvp[i][1])
        i += 1
    for key in kvp:
        if dc.has_key(key[0]):
            if key[1] > dc[key[0]]:
                dc[key[0]] = key[1]
        else:
            dc[key[0]] = key[1]
    ret = ''
    for key in dc.keys():
        ret += "{}, {}\r\n".format(key, dc[key])
    print ret
    return 0        

if __name__ == "__main__":
    main()
    
