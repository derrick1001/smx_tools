#!/usr/bin/python3

import re
from sys import argv

from calix.affected_decorator import affected_decorator
from calix.connection import calix_e9
from calix.crayon import c_BLUE

# NOTE:
#   Call this script with the IP address and hostname
#   of the chassis


def proc_alarms(func):
    @affected_decorator
    def inner(**kwargs):
        alrm_tbl = func()
        match = [re.search("'[0-9]{1,5}'", alrm) for alrm in alrm_tbl.split("\n")]
        ont_id = [m.group().lstrip("'").rstrip("'") for m in match if m is not None]
        return ont_id

    return inner


@proc_alarms
def alarm_table(e9=argv[2]):
    cnct = calix_e9()
    tbl = input("Alarm name: ")
    dying = cnct.send_command_timing("show alarm active | include dying")
    missing = cnct.send_command_timing("show alarm active | include missing")

    # NOTE: Send this through another decorator first to get the ont_ids
    lop = cnct.send_command_timing("show alarm active | include loss")
    if tbl == "dying":
        return dying
    elif tbl == "missing":
        return missing
    else:
        print('Please use "dying" or "missing"')
        alarm_table(e9=argv[2])


if __name__ == "__main__":
    alarm_table(e9=argv[2])
    # q = input("Press any key to exit...")
    # if q:
    #    quit()
