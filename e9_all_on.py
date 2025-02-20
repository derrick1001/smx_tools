#!/usr/bin/python3

from sys import argv

from netmiko import ConnectHandler

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
    with ConnectHandler(**device) as cnct:
        cnct.send_command_timing("configure")
        for shelf in shelves:
            for sl in slot:
                card = cnct.send_command_timing(
                    f"do show card {shelf}/{sl} |\
                notab | include provision"
                )
                print(f"{shelf}/{sl}")
                if "NG1601" in card.split()[1]:
                    print("Card is 1601")
                    port = range(15, 17)
                else:
                    print("Card is 3201")
                    port = range(1, 33)
                for p in port:
                    cnct.send_command_timing(f"interface pon {shelf}/{sl}/xp{p}")
                    cnct.send_command_timing(f"interface pon {shelf}/{sl}/xp{p}")
                    cnct.send_command_timing("no shutdown")
                    cnct.send_command_timing("top")
                    print(f"{shelf}/{sl}/xp{p} is on")


if __name__ == "__main__":
    turn_on_ports()
