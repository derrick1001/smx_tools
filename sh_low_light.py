#!/usr/local/bin/python3

from calix.connection import calix_e9


def low_light():
    cnct = calix_e9()
    no_last = slice(None, -1)

    output = cnct.send_command_timing("show alarm act | inc low")
    for line in output.split("\n")[no_last]:
        print(line)
    print(len(output.split("\n")[no_last]), "Alarms")
    q = input("Press any key to exit...")
    if q == "":
        exit()
    else:
        exit()


low_light()
