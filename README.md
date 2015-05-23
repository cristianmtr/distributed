distributed
=======

Project for learning distributed systems architecture

Test case for cities - temperatures case:

```
cd key_value_temperatures/

./test_case.py <nr of workers>
```

Tested on Windows and Linux. 


DEPENDENCIES
====
The basic programs will run both on Windows and Linux.

However, the test_case will require the psutil module.

In order to compile the c++ python module do the following:
```
python setup.py build

cp build/lib*/module.so ./
```
If you're having issues compiling, just use the extract_tasks_and_input() function defined in server.py instead of the module.my_extract()


TODO
=====
- to read more papers on MR, HDFS;
- each worker to store a shard of data;
- master node to store index of what each worker has;
- display information via HTTP;
- allow for task execution via HTTP forms;







