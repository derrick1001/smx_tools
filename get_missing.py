#!/usr/bin/python3

from sys import argv

from calix.connection import calix_e9
from calix.proc_alrms import proc_alarms
from crayon import c_BLUE, c_WHITE, c_YELLOW

# NOTE:
#   Call this script with the IP address and hostname
#   of the chassis


@proc_alarms
def alarm_table(e9=argv[2]):
    cnct = calix_e9()
    tbl = input(f"{c_BLUE}Alarm name: {c_WHITE}")
    if tbl == "dying":
        dying = cnct.send_command_timing("show alarm active | include ont-dying-gasp")
        cnct.disconnect()
        return dying
    elif tbl == "missing":
        missing = cnct.send_command_timing("show alarm active | include missing")
        cnct.disconnect()
        return missing
    elif tbl == "red":
        red_temp = cnct.send_command_timing("show alarm active | include red-temp")
        cnct.disconnect()
        return red_temp
    elif tbl == "all":
        alrms = cnct.send_command_timing(
            'show alarm active | include "dying|missing|red-temp"'
        )
        cnct.disconnect()
        return alrms
    elif tbl == "lop":
        lop = cnct.send_command_timing("show alarm active | include loss-of-pon")
        return lop
    else:
        print('Valid completions: "all", "dying", "missing", "lop", "red"')
        alarm_table(e9=argv[2])


if __name__ == "__main__":
    subs = alarm_table(e9=argv[2])
    count = 0
    for sub in subs:
        print(sub)
        count += 1
    print(f"{c_YELLOW}{count} Alarms")
