#!/usr/bin/python3

from netmiko import ConnectHandler
from requests import get
from sys import argv, path


# Call script with IP address, hostname


def get_info():
    path.append('/home/derrick/Derrick-shell-scripts/python/modules/')
    from crayon import c_BLUE, c_WHITE
    shelf = (input(f'{c_BLUE}Shelf: {c_WHITE}'))
    slot = (input(f'{c_BLUE}Slot: {c_WHITE}'))
    port = (input(f'{c_BLUE}Port: {c_WHITE}'))
    return shelf, slot, port


def get_act(func):
    def wrapper(*args):
        onts = func(*args)
        if isinstance(onts, list):
            for id in onts:
                get_cx = get(f'https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{argv[2]}/port/{id}%2Fx1',
                             auth=('admin', 'Thesearethetimes!'),
                             verify=False)
                r = get_cx.json()
                if r.get('locations') is None:
                    continue
                loc, city, state, z = r.get('locations')[
                    0].get('address')[0].values()
                print(r.get('customId'))
                print(r.get('name'))
                print(loc)
                print(f'{city} {state} {z}\n')

        else:
            print('Went here')
            for lst in onts:
                for id in lst:
                    get_phone = get(f'https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{argv[2]}/port/{id}%2Fx1',
                                    auth=('admin', 'Thesearethetimes!'),
                                    verify=False)
                    r = get_phone.json()
                    if r.get('locations') is None:
                        continue
                    loc, city, state, z = r.get('locations')[
                        0].get('address')[0].values()
                    print(r.get('customId'))
                    print(r.get('name'))
                    print(loc)
                    print(f'{city} {state} {z}\n')
        return onts
    return wrapper


def get_miss(func):
    def wrapper1(*args):
        print('This is the get_miss function')
        onts = func(*args)
        missing = get(f'https://10.20.7.10:18443/rest/v1/config/device/{argv[2]}/ont/missingONTs?offset=0&limit=20',
                      auth=('admin', 'Thesearethetimes!'),
                      verify=False)
        r = missing.json()
        for i in r:
            ont_id = i.get('ont-id')
            print(ont_id)
        return onts
    return wrapper1


@get_act
def netcon(shelf, slot, port):
    device = {'device_type': 'cisco_ios',
              'host':   f'{argv[1]}',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }
    ports = range(1, 17)
    slots = range(1, 3)
    cnct = ConnectHandler(**device)
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
    return onts


shelf, slot, port = get_info()
netcon(shelf, slot, port)
