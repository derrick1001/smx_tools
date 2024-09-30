#!/usr/bin/python3

from netmiko import ConnectHandler
from requests import get
from sys import argv, path


def get_info():
    path.append('/home/derrick/Derrick-shell-scripts/python/modules/')
    from crayon import c_BLUE, c_WHITE
    shelf = (input(f'{c_BLUE}Shelf: {c_WHITE}'))
    slot = (input(f'{c_BLUE}Slot: {c_WHITE}'))
    port = (input(f'{c_BLUE}Port: {c_WHITE}'))
    return shelf, slot, port


def get_cx(func):
    def wrapper(*args, **kwargs):
        print('This is the wrapper func')
        print(f'These are netcons args: {args}, and kwargs: {kwargs}')
        result = func(*args, **kwargs)
        print(result)
        return result
    return wrapper


@get_cx
def netcon(shelf, slot, port):
    device = {'device_type': 'cisco_ios',
              'host':   f'{argv[1]}',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }
    ports = range(1, 17)
    slots = range(1, 3)
    with ConnectHandler(**device) as cnct:
        if not slot == "" and port == "":
            onts = (cnct.send_command_timing(
                f'show interface pon {shelf}/{slot}/xp{p} ranged-onts \
                statistics | inc ont-id').split()[1::2]
                for p in ports)
        elif slot == "":
            onts = (cnct.send_command_timing(
                f'show interface pon {shelf}/{sl}/xp{p} ranged-onts \
                statistics | inc ont-id').split()[1::2]
                for sl in slots
                for p in ports)
        else:
            onts = cnct.send_command_timing(
                f'show interface pon {shelf}/{slot}/xp{port} ranged-onts \
                statistics | inc ont-id').split()[1::2]
        cnct.send_command_timing('configure')
        e9 = cnct.send_command_timing(
            'show full-configuration hostname').split('\n')[0].lstrip('hostname ')
        cnct.send_command_timing('exit')
    return onts, e9


shelf, slot, port = get_info()
netcon(shelf, slot, port)
