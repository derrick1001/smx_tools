#!/usr/bin/python3

import re
from sys import argv

from calix.affected_decorator import affected_decorator
from calix.connection import calix_e9

# NOTE:
#   Call this script with the IP address and hostname
#   of the chassis


def proc_alarms(func):
    @affected_decorator
    def inner(**kwargs):
        miss_gasp = func()
        match = [re.search("'[0-9]{1,5}'", alrm) for alrm in miss_gasp.split("\n")]
        ont_id = [m.group().lstrip("'").rstrip("'") for m in match if m is not None]
        return ont_id

    return inner


@proc_alarms
def alarm_table(e9=argv[2]):
    cnct = calix_e9()
    missing_gasp = cnct.send_command_timing(
        'show alarm active | include "dying|missing"'
    )
    return missing_gasp


if __name__ == "__main__":
    from crayon import c_CYAN, c_YELLOW

    subs = alarm_table(e9=argv[2])
    count = 0
    for sub in subs:
        print("")
        print(sub)
        count += 1
    print(f"{c_YELLOW}{count} Alarms")
    q = input(f"{c_CYAN}Press any key to exit...")
    if q:
        quit()
