from time import sleep

from netmiko import ConnectHandler

f1 = "n1"
f2 = "w2"
f3 = "s3"
f4 = "xw2"
ports = range(1, 24, 2)
fibers = (f for f in range(117, 142) if f % 12 != 0)
# for p in ports:
#    print(f"5/1/xp{p}_{f4},{next(fibers)}-{next(fibers)}")

device = {
    "device_type": "cisco_ios",
    "host": "10.20.5.51",
    "username": "sysadmin",
    "password": "Thesearethetimes!",
    "fast_cli": False,
}
cnct = ConnectHandler(**device)

for p in ports:
    cnct.send_command_timing("configure")
    cnct.send_command_timing(f"interface pon 5/2/xp{p}")
    cnct.send_command_timing(f"description {f4},{next(fibers)}-{next(fibers)}")
    output = cnct.send_command_timing(f"top show full-configuration int pon 5/2/xp{p}")
    print(output)
    sleep(1)
    print("")
