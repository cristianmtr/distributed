#!/bin/bash
# python server.py > server.log &
python worker.py > worker.log &
python requester.py key_value_temperatures/map.py key_value_temperatures/map.input key_value_temperatures/distributor.py key_value_temperatures/reduce.py
