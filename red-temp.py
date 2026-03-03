#!/usr/local/bin/python3

from sys import argv

from calix.connection import calix_e9
from calix.e_mail import email
from calix.proc_alrms import proc_alarms


@proc_alarms
def red_temp_alrm(e9=argv[2]):
    cnct = calix_e9()
    red_temp = cnct.send_command_timing("show alarm active | include red-temp")
    cnct.disconnect()
    return red_temp


if __name__ == "__main__":
    sub = red_temp_alrm(e9=argv[2])
    subj = "ONT red temp alarm"
    email(subj, next(sub))
