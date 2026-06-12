#!/usr/bin/env python3


from sys import argv
from calix.e9 import CalixE9
from calix.axos_e9 import device


def alarm_table(name: str) -> str:
    match name:
        case "dying":
            dying = e9.alrm_dying()
            return dying
        case "missing":
            missing = e9.alrm_missing()
            return missing
        case "red":
            red_temp = e9.alrm_red_temp()
            return red_temp
        case "lop":
            lop = e9.alrm_loss_of_pon()
            return lop


if __name__ == "__main__":
    e9 = CalixE9(device(argv[1]))
    data = alarm_table(argv[2])
    subs = e9.get_subs(data)
    for count, sub in enumerate(subs):
        print(sub)
    if 'count' in locals():
        print(f"There are {count + 1} sub(s)")
