#!/usr/bin/python3

from calix.cx_detail import cx
from calix.ont_detail import ont


r = cx("Liberty-E9-1", "82")
a = ont("Liberty-E9-1", "82")
print(f"{r}\n")
print(a.get("oper-status"))
