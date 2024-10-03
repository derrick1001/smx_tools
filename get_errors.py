#!/usr/bin/python3

import re
from netmiko import ConnectHandler
from sys import argv, path
from requests import get


def get_port():
    path.append('/home/derrick/Derrick-shell-scripts/python/modules/')
    from crayon import c_BLUE, c_WHITE
    shelf = (input(f'{c_BLUE}Shelf: {c_WHITE}'))
    slot = (input(f'{c_BLUE}Slot: {c_WHITE}'))
    port = (input(f'{c_BLUE}Port: {c_WHITE}'))
    return shelf, slot, port


def netcon(shelf, slot, port):
    device = {'device_type': 'cisco_ios',
              'host':   f'{argv[1]}',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }
    with ConnectHandler(**device) as cnct:
        ranged_ont = cnct.send_command_timing(
            f'show interface pon {shelf}/{slot}/xp{port} ranged-onts statistics')
        # Get hostname so we can call the API in test(func). test(func) is gonna decorate the main()
        cnct.send_command_timing('configure')
        e9 = cnct.send_command_timing(
            'show full-configuration hostname').split('\n')[0].lstrip('hostname ')
        cnct.send_command_timing('exit')
    return ranged_ont, e9


def test(str1, e9):
    m = re.split(r'ont CXNK [A-Z0-9]{6,7}', str1)
    m_lst = (i.split() for i in m[1:])
    ranged_onts = (dict(zip(i[::2], i[1::2])) for i in m_lst)
    return ranged_onts


def main(dict0):
    from crayon import c_BLUE, c_GREEN, c_YELLOW, c_RED, c_CYAN, c_MAGENTA
    for i in dict0:
        ont_id = i.get('ont-id')
        get_name = get(f'https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{ont_id}%2Fx1',
                       auth=('admin', 'Thesearethetimes!'),
                       verify=False)
        r = get_name.json()
        name = r.get('name')
        print(f'{c_CYAN}{name}')
        for k, v in i.items():
            if k == 'ranged-onts':
                continue
            if k == 'ont-id':
                print(f'{c_BLUE}{k}\t\t{c_GREEN}{v}')
                continue
            if 'errors' in k:
                numv = int(v)
                if numv == 0:
                    print(f'{c_BLUE}{k}\t{c_MAGENTA}{v}')
                else:
                    print(f'{c_BLUE}{k}\t{c_RED}{v}')
                continue
            if k == 'ds-sdber-rate':
                print(f'{c_BLUE}{k}\t{c_YELLOW}{v}\n')
                continue
            print(f'{c_BLUE}{k}\t{c_YELLOW}{v}')
    q = input(f'{c_CYAN}Press enter to exit...')
    if q is None:
        exit()


shelf, slot, port = get_port()
str1, e9 = netcon(shelf, slot, port)
a = test(str1, e9)
main(a)
