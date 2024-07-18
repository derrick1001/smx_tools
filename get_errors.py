#!/usr/bin/python3

import re
from crayon import c_BLUE, c_GREEN, c_YELLOW, c_RED, c_WHITE
from netmiko import ConnectHandler
from sys import argv


def get_err():
    shelf = input(f'{c_BLUE}Shelf: {c_WHITE}')
    slot = input(f'{c_BLUE}Slot: {c_WHITE}')
    port = input(f'{c_BLUE}Port: {c_WHITE}')
    return shelf, slot, port


def netcon(shelf, slot, port):
    device = {'device_type': 'cisco_ios',
              'host':   f'{argv[1]}',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }
    con = ConnectHandler(**device)
    output = con.send_command_timing(
        f'show interface pon {shelf}/{slot}/{port} ranged-onts statistics')
    return output


shelf, slot, port = get_err()
str1 = netcon(shelf, slot, port)
m = re.split(r'ont CXNK [A-Z0-9]{6,7}', str1)
print('')
for i in m:
    tmp = i.split()
    ndict = dict(zip(tmp[::2], tmp[1::2]))
    for k, v in ndict.items():
        if k == 'ranged-onts':
            continue
        if k == 'ont-id':
            print(f'{c_BLUE}{k}\t\t{c_GREEN}{v}')
            continue
        if 'errors' in k:
            print(f'{c_BLUE}{k}\t{c_RED}{v}')
            continue
        if k == 'ds-sdber-rate':
            print(f'{c_BLUE}{k}\t{c_YELLOW}{v}\n')
            continue
        print(f'{c_BLUE}{k}\t{c_YELLOW}{v}')
