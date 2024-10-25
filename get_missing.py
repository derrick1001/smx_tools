#!/usr/bin/python3

from sys import argv
import re

from calix.connection import calix_e9
from calix.affected_decorator import affected_decorator

# NOTE:
#   Call this script with the IP address and hostname
#   of the chassis


def proc_alarms(func):
    @affected_decorator
    def inner(**kwargs):
        miss_gasp = func()
        match = [re.search("'[0-9]{1,5}'", alrm)
                 for alrm in miss_gasp.split('\n')]
        ont_id = [m.group().lstrip("'").rstrip("'")
                  for m in match if m is not None]
        return ont_id
    return inner


@proc_alarms
def alarm_table(e9=argv[2]):
    cnct = calix_e9()
    missing_gasp = cnct.send_command_timing(
        'show alarm active | include "dying|missing"')
    return missing_gasp


if __name__ == '__main__':
    alarm_table(e9=argv[2])
