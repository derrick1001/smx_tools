#!/usr/bin/python3

from sys import argv

from calix.connection import calix_e9
from calix.e_mail import email
from calix.proc_alrms import proc_alarms


@proc_alarms
def rogue(e9=argv[2]):
    cnct = calix_e9()
    red_temp = cnct.send_command_timing(
        "show alarm active | include ont-rogue-detected"
    )
    cnct.disconnect()
    return rogue


if __name__ == "__main__":
    sub = rogue(e9=argv[2])
    subj = f"Rogue ONT detected on {argv[2]}"
    email(subj, next(sub))
