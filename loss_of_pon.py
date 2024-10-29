#!/usr/bin/python3

import re

from calix.affected_decorator import affected_decorator
from calix.connection import calix_e9

lop = "ne-event-time 2024-10-28T15:23:45-05:00 id 5005 instance-id 7.156026 name loss-of-pon perceived-severity MAJOR category PON address /config/interface/pon[port='4/1/xp10']"
match = [re.search("[2-5]/[1-2]/xp[0-9]{1,2}", alrm) for alrm in lop.split("\n")]
pon_port = [m.group().lstrip("'").rstrip("'") for m in match if m is not None]
cnct = calix_e9()
m = [
    cnct.send_command_timing(
        f"show interface pon {port} subscriber-info | display curly-braces | include ont"
    )
    for port in pon_port
]
m1 = (re.findall("[0-9]{4,5}", id) for id in m)


@affected_decorator
def f1(e9="Hammett-E9-1"):
    m1 = (re.findall("[0-9]{4,5}", id) for id in m)
    return next(m1)


f1(e9="Hammett-E9-1")
