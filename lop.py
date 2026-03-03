#!/usr/local/bin/python3

from subprocess import run
from sys import argv

from calix.connection import calix_e9
from calix.e_mail import email
from calix.proc_alrms import proc_alarms


@proc_alarms
def alrm_tbl(e9=argv[2]):
    cnct = calix_e9()
    lop = cnct.send_command_timing("show alarm active | include loss-of-pon")
    cnct.disconnect()
    return lop


if __name__ == "__main__":
    subs = alrm_tbl(e9=argv[2])
    with open("lop_subs.txt", "a") as f:
        for sub in subs:
            f.write(f"{sub}\n")
    with open("lop_subs.txt", "r+") as f:
        email(f"Loss of PON on {argv[2]}", f.read())
    run("rm lop_subs.txt", shell=True)
