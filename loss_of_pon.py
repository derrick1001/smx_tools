#!/usr/bin/python3

from sys import argv

from calix.connection import calix_e9
from calix.proc_alrms import proc_alarms
from crayon import c_YELLOW


@proc_alarms
def alrm_tbl(e9=argv[2]):
    cnct = calix_e9()
    lop = cnct.send_command_timing("show alarm active | include loss-of-pon")
    cnct.disconnect()
    return lop


if __name__ == "__main__":
    subs = alrm_tbl(e9=argv[2])
    for count, sub in enumerate(subs):
        print(sub)
    print(f"{c_YELLOW}{count} Alarms")
