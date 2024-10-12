#!/usr/bin/python3


from sys import path

path.append("/home/derrick/Derrick-shell-scripts/python/modules/")


def low_light():
    from calix import netcon

    cnct = netcon()
    no_last = slice(None, -1)

    output = cnct.send_command_timing("show alarm act | inc red")
    for line in output.split("\n")[no_last]:
        print(line)
    print(len(output.split("\n")[no_last]), "Alarms")
    q = input("Press any key to exit...")
    if q == "":
        exit()
    else:
        exit()


low_light()
