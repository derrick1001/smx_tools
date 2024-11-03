#!/usr/bin/python3

from requests import get
from sys import argv
from calix import ssp, netcon


# NOTE: Call script with IP address, hostname


def get_act(func):
    def wrapper(*args):
        onts = func(*args)
        if isinstance(onts, list):
            for id in onts:
                get_cx = get(
                    f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{argv[2]}/port/{id}%2Fx1",
                    auth=("admin", "Thesearethetimes!"),
                    verify=False,
                )
                r = get_cx.json()
                if r.get("locations") is None:
                    continue
                loc, city, state, z = r.get("locations")[0].get("address")[0].values()
                print(r.get("customId"))
                print(r.get("name"))
                print(loc)
                print(f"{city} {state} {z}\n")

        else:
            print("Went here")
            for lst in onts:
                if lst is None:
                    continue
                for id in lst:
                    get_cx = get(
                        f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{argv[2]}/port/{id}%2Fx1",
                        auth=("admin", "Thesearethetimes!"),
                        verify=False,
                    )
                    r = get_cx.json()
                    if r.get("locations") is None:
                        continue
                    loc, city, state, z = (
                        r.get("locations")[0].get("address")[0].values()
                    )
                    print(r.get("customId"))
                    print(r.get("name"))
                    print(loc)
                    print(f"{city} {state} {z}\n")
        return onts

    return wrapper


@get_act
def get_miss(main_f):
    def missing():
        func = main_f()


# @get_act
def main():  # NOTE: Returns list[lists], or a single list
    shelf, slot, port = ssp()
    cnct = netcon()
    ports = range(1, 17)
    slots = range(1, 3)
    step_2 = slice(1, None, 2)
    if not slot == "" and port == "":
        onts = (
            cnct.send_command_timing(
                f"show interface pon {shelf}/{slot}/xp{p} ranged-onts \
            statistics | inc ont-id"
            ).split()[step_2]
            for p in ports
        )
    elif slot == "":
        onts = (
            cnct.send_command_timing(
                f"show interface pon {shelf}/{sl}/xp{p} ranged-onts \
            statistics | inc ont-id"
            ).split()[step_2]
            for sl in slots
            for p in ports
        )
    else:
        onts = cnct.send_command_timing(
            f"show interface pon {shelf}/{slot}/xp{port} ranged-onts \
            statistics | inc ont-id"
        ).split()[step_2]
    return onts


main()