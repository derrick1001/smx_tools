#!/usr/local/bin/python3.13

from calix.connection import calix_e9

cnct = calix_e9()

slots = range(1, 3)
xports = range(1, 9)
gports = range(1, 3)

cnct.send_command_timing('configure')
for slot in slots:
    for port in xports:
        cnct.send_command_timing(f"interface ethernet 1/{slot}/x{port}")
        cnct.send_command_timing('shutdown')
        cnct.send_command_timing('exit', strip_prompt=True)
        print(f"1/{slot}/x{port} is shutdown")
for slot in slots:
    for port in gports:
        cnct.send_command_timing(f"interface ethernet 1/{slot}/g{port}")
        cnct.send_command_timing('shutdown')
        cnct.send_command_timing('exit', strip_prompt=True)
        print(f"1/{slot}/g{port} is shutdown")
cnct.disconnect()
