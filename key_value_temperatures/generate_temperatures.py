from random import randint
import itertools
import sys

if len(sys.argv) < 2:
    print "Usage: python generate_temperatures.py <nr_of_entries>"
    sys.exit(1)
entries = int(sys.argv[1])
cities = ['Rome', 'Copenhagen', 'Toronto', 'Tokyo', 'Rio de Janeiro', 'Sydney']
cities = itertools.cycle(cities)
with open("map.input", "w") as f:
    i = 0
    city = cities.next()
    while i < entries:
        if city == "Rome":
            f.write("{}, {}\r\n".format(city, randint(5, 45)))
        elif city == "Copenhagen":
            f.write("{}, {}\r\n".format(city, randint(-30, 35)))
        elif city == "Toronto":
            f.write("{}, {}\r\n".format(city, randint(-50, 14)))
        elif city == "Rio de Janeiro":
            f.write("{}, {}\r\n".format(city, randint(10, 55)))
        elif city == "Sydney":
            f.write("{}, {}\r\n".format(city, randint(10, 50)))
        elif city == "Tokyo":
            f.write("{}, {}\r\n".format(city, randint(-20, 40)))
        i += 1
        city = cities.next()
        
