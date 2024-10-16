#!/usr/bin/python3

from sys import argv

from calix.cx_detail import cx
from calix.ont_detail import ont
from calix.connection import calix_e9
from calix.affected import affected


@affected
def f(a, b, c):
    pass


a = f("Seminole-E9-1", ["10.33491", "10.33765"], "11518")
print(a)
