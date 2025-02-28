#!/usr/bin/python3

from subprocess import run
from sys import argv

from calix.connection import calix_e9
from calix.e_mail import email
from calix.proc_alrms import proc_alarms


@proc_alarms
def alrm_tbl(e9=argv[2]):
    cnct = calix_e9()
    pmd = cnct.send_command_timing("show alarm active | include pon-mac-degraded")
    cnct.disconnect()
    return pmd


if __name__ == "__main__":
    subs = alrm_tbl(e9=argv[2])
    with open("pmd_subs.txt", "a") as f:
        for sub in subs:
            f.write(f"{sub}\n")
    with open("pmd_subs.txt", "r+") as f:
        email(f"PON mac degraded on {argv[2]}", f.read())
    run("rm pmd_subs.txt", shell=True)
