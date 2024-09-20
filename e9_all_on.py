#!/usr/bin/python3

from netmiko import ConnectHandler
from sys import argv


def connect():
    device = {'device_type': 'cisco_ios',
              'host':   '192.168.1.1',
              'username':   'sysadmin',
              'password':   'sysadmin',
              'fast_cli':   False,
              }

    cnct = ConnectHandler(**device)
    return cnct


def shelf():
    # configure
    # interface pon x/x/x
    # no shut
    # top
    shelves = int(argv[1])
    with connect() as cnct:
        cnct.send_command_timing('configure')
        for shelf in shelves:
            for p in range(1, 17):
                for sl in range(1, 3):
                    cnct.send_command_timing(
                        f'interface pon {shelf}/{sl}/xp{p}')
                    cnct.send_command_timing('shutdown')
                    cnct.send_command_timing('top')
