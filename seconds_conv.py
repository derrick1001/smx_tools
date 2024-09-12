#!/usr/bin/python3

from datetime import timedelta

sec = 828164
print('Time in seconds: ', sec)

td = timedelta(seconds=sec)
td_str = str(td)
tmp = td_str.split(':')
h, m, s = tmp
print(f'{h} hours, {m} minutes, {s} seconds')
