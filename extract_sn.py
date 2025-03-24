#!/usr/local/bin/python3

import re

with open("calix-sn.txt") as f:
    for line in f:
        m = re.search("sn=\\d{12}", line)
        if m:
            print(m.group().lstrip("sn="))
