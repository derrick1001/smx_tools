#!/usr/local/bin/python3

from subprocess import run
from sys import argv

from calix.connection import calix_e9
from calix.e_mail import email
from calix.proc_alrms import proc_alarms


@proc_alarms
def rogue(e9=argv[2]):
    cnct = calix_e9()
    rogue_alrm = cnct.send_command_timing(
        "show alarm active | include ont-rogue-detected"
    )
    cnct.disconnect()
    return rogue_alrm


if __name__ == "__main__":
    subs = rogue(e9=argv[2])
    with open("rogues.txt", "a") as f:
        for sub in subs:
            f.write(f"{sub}\n")
    with open("rogues.txt", "r+") as f:
        email(f"Rogue ONTs detected on {argv[2]}", f.read())
    run("rm rogues.txt", shell=True)
