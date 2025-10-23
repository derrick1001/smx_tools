#!/usr/local/bin/python3.13

from sys import argv
from calix.e9 import CalixE9

e9 = CalixE9(argv[1], argv[2])

xports = e9.eth_range("x")
gports = e9.eth_range("g")

e9.connection.send_command_timing("configure")
for port in xports:
    cmd = [f"interface ethernet {port}\nshutdown\nexit"]
    e9.connection.send_command_timing(cmd[0])
    print(f"{port} is shutdown")
for port in gports:
    cmd = [f"interface ethernet {port}\nshutdown\nexit"]
    e9.connection.send_command_timing(cmd[0])
    print(f"{port} is shutdown")
