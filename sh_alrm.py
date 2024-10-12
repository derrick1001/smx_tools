#!/usr/bin/python3


from sys import path

path.append("/home/derrick/Derrick-shell-scripts/python/modules/")


def low_light():
    from calix import netcon

    cnct = netcon()

    output = cnct.send_command_timing("show alarm act | inc low")
    for line in output.split("\n")[:-1]:
        print(line)
    print(len(output.split("\n")[:-1]), "Alarms")
    q = input("Press any key to exit")
    if q == "":
        exit()
    else:
        exit()


low_light()
