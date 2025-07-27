#!/usr/local/bin/python3

from sys import argv
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def default_or_not():
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "sysadmin",
        "password": "sysadmin",
        "fast_cli": True,
    }
    device_configured = {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "sysadmin",
        "password": "Thesearethetimes!",
        "fast_cli": True,
    }
    try:
        cnct = ConnectHandler(**device)
        return cnct
    except NetmikoTimeoutException:
        print("Network not reachable, check network settings")
    except NetmikoAuthenticationException:
        return ConnectHandler(**device_configured)


def turn_on_ports(cnct, start: int, stop: int):
    shelves = range(start, stop + 1)
    slot = range(1, 3)
    with cnct:
        cnct.send_command_timing("configure")
        for shelf in shelves:
            for sl in slot:
                card = cnct.send_command_timing(
                    f"do show card {shelf}/{sl} |\
                notab | include provision"
                )
                if "NG1601" in card.split()[1]:
                    print(f"{shelf}/{sl} card is 1601")
                    port = range(1, 17)
                elif "XG3201" in card.split()[1]:
                    print(f"{shelf}/{sl} card is 3201")
                    port = range(1, 33)
                else:
                    print("Card not in service, use show card to verify")
                for p in port:
                    cmd_list = [f"interface pon {shelf}/{sl}/xp{p}\nno shutdown\ntop"]
                    cnct.send_command_timing(cmd_list[0])
                    print(f"{shelf}/{sl}/xp{p} is on")


if __name__ == "__main__":
    try:
        int(argv[1]) and int(argv[2]) in range(2, 6)
        cnct = default_or_not()
        if cnct is not None:
            turn_on_ports(cnct, int(argv[1]), int(argv[2]))
    except ValueError:
        print("Wrong format, use command python3 e9_all_on.py <2-5> <2-5>")
