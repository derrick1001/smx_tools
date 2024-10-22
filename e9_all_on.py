#!/usr/bin/python3

from netmiko import ConnectHandler
from sys import argv

#   TODO:
#   Add functionality for 3201 cards
#   Test to see if threading will speed this up


def turn_on_ports():  # NOTE: Call with starting shelf and ending shelf
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "sysadmin",
        "password": "sysadmin",
        "fast_cli": False,
    }
    shelves = range(int(argv[1]), int(argv[2]) + 1)
    slot = range(1, 3)
    port = range(1, 17)
    with ConnectHandler(**device) as cnct:
        cnct.send_command_timing("configure")
        for shelf in shelves:
            for sl in slot:
                for p in port:
                    cnct.send_command_timing(
                        f"interface pon {shelf}/{sl}/xp{p}")
                    cnct.send_command_timing(
                        f"interface pon {shelf}/{sl}/xp{p}")
                    cnct.send_command_timing("no shutdown")
                    cnct.send_command_timing("top")
                    print(f"{shelf}/{sl}/xp{p} is on")


if __name__ == "__main__":
    turn_on_ports()
