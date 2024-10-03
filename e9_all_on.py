#!/usr/bin/python3

from netmiko import ConnectHandler
from sys import argv

# Add functionality for 3201 cards


# Call with target IP and number of shelves
def shelf():
    device = {'device_type': 'cisco_ios',
              'host':   argv[1],
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }
    shelves = range(2, int(argv[2]) + 1)
    slot = range(1, 3)
    port = range(1, 17)
    with ConnectHandler(**device) as cnct:
        cnct.send_command_timing('configure')
        for shelf in shelves:
            for sl in slot:
                for p in port:
                    cnct.send_command_timing(
                        f'interface pon {shelf}/{sl}/xp{p}')
                    cnct.send_command_timing('shutdown')
                    cnct.send_command_timing('top')


if __name__ == '__main__':
    shelf()
