#!/usr/bin/python3

import re
from sys import argv

from calix.affected_decorator import affected_decorator
from calix.connection import calix_e9
from crayon import c_BLUE, c_WHITE, c_YELLOW

# NOTE:
#   Call this script with the IP address and hostname
#   of the chassis


def proc_alarms(func):
    @affected_decorator
    def inner(**kwargs):
        alrm_tbl = func()
        if "loss-of-pon" in alrm_tbl:
            match_pon = [
                re.search("[2-5]/[1-2]/xp[0-9]{1,2}", alrm)
                for alrm in alrm_tbl.split("\n")
            ]
            pon_port = [
                m.group().lstrip("'").rstrip("'") for m in match_pon if m is not None
            ]
            cnct = calix_e9()
            sub_on_port = [
                cnct.send_command_timing(
                    f"show interface pon {port} subscriber-info | display curly-braces | include ont"
                )
                for port in pon_port
            ]
            match_ont = [re.search("[0-9]{1,5}", id) for id in sub_on_port]
            ont_id = [
                m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None
            ]
            return ont_id
        else:
            match_ont = [
                re.search("'[0-9]{1,5}'", alrm) for alrm in alrm_tbl.split("\n")
            ]
            ont_id = [
                m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None
            ]
            return ont_id

    return inner


@proc_alarms
def alarm_table(e9=argv[2]):
    cnct = calix_e9()
    tbl = input(f"{c_BLUE}Alarm name: {c_WHITE}")
    if tbl == "dying":
        dying = cnct.send_command_timing("show alarm active | include dying")
        cnct.disconnect()
        return dying
    elif tbl == "missing":
        missing = cnct.send_command_timing("show alarm active | include missing")
        cnct.disconnect()
        return missing
    elif tbl == "lop":
        lop = cnct.send_command_timing("show alarm active | include loss")
        return lop
    else:
        print('Valid completions: "dying", "missing", "lop"')
        alarm_table(e9=argv[2])


if __name__ == "__main__":
    subs = alarm_table(e9=argv[2])
    count = 0
    for sub in subs:
        print("")
        print(sub)
        count += 1
    print(f"{c_YELLOW}{count} Alarms")
