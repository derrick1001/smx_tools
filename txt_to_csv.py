#!/usr/bin/python3

import csv

data = [["Acct", "Name", "Phone", "Port/Fiber", "Email", "Address"]]
a = """1700007891
JASON FLY
4054712450
2/2/xp13 -> n3-62,63
jfly582@gmail.com
32757 HWY 9, TECUMSEH

1700023685
MONICA M DOSH
No phone
2/2/xp13 -> n3-62,63
MONICADOSH6@GMAIL.COM
33215 SKYRIDGE DR, TECUMSEH

1700012643
YESICA MEDINA
9186195123
2/2/xp13 -> n3-62,63
diazjoseg89@gmail.com
21351 SKYVIEW DR, TECUMSEH

1700012643
YESICA MEDINA
9186195123
2/2/xp13 -> n3-62,63
diazjoseg89@gmail.com
21351 SKYVIEW DR, TECUMSEH

1700013807
LAURA MCMASTERS
4054305954
2/2/xp13 -> n3-62,63
vickimitchell82@gmail.com
21983 SKYVIEW DR, TECUMSEH

1700004916
NIKKI D SHEPHERD
No phone
2/2/xp13 -> n3-62,63
nikkishepherd@yahoo.com
21399 SKYVIEW DR, TECUMSEH

1700014197
SERGIO LOPEZ
4054962935
2/2/xp13 -> n3-62,63
lopez.ortiz.sg@gmail.com
33384 SKYRIDGE DR, TECUMSEH

1700014524
BREANN JOHNSON
No phone
2/2/xp13 -> n3-62,63
navyrotccadet890@yahoo.com
TRAILER, TECUMSEH

1700015093
ROBERT R SMITH
4054816004
2/2/xp13 -> n3-62,63
smith13rs2003@gmail.com
21362 SKY VIEW DR, TECUMSEH

1700017755
SARAH A BUTTRAM
No phone
2/2/xp13 -> n3-62,63
sarahanne854@yahoo.com
21268 SKYVIEW DR, TECUMSEH

1700023908
COLBY J WALLER
No phone
2/2/xp13 -> n3-62,63
CJHALL45@GMAIL.COM
22017 STEVENS RD, TECUMSEH

1700002847
RICKY J GAGE
4055986904
2/2/xp13 -> n3-62,63
joegage@windstream.net
22010 STEVENS RD, TECUMSEH

1700003230
SHAWNA PARKS
No phone
2/2/xp13 -> n3-62,63
parksmed170@gmail.com
21627 STEVENS RD-BARN, TECUMSEH

1700006265
FORD A BUCHANAN
No phone
2/2/xp13 -> n3-62,63
f589buchanan@gmail.com
33385 SKYRIDGE DR, TECUMSEH

1700006513
RYAN K ALRED
No phone
2/2/xp13 -> n3-62,63
falconof73@live.com
21249 STEVENS RD, TECUMSEH

1700003263
JAMES MEEKS
4059240647
2/2/xp13 -> n3-62,63
jameslintx@hotmail.com
33372 SKYRIDGE DR, TECUMSEH

1700010529
RICK A THORNBURG
4055985936
2/2/xp13 -> n3-62,63
rthornburg837@gmail.com
21617 STEVENS RD-HOUSE, TECUMSEH

1700010240
GREG R MORROW
9184244478
2/2/xp13 -> n3-62,63
jodykay72@gmail.com
21428 SKYVIEW DR, TECUMSEH"""


def func():
    count = 18
    s = 0
    f = 6
    sl = slice(s, f)
    while count > 0:
        sl = slice(s, f)
        b = a.split("\n")[sl]
        s += 7
        f += 7
        count -= 1
        yield b


z = func()
for i in z:
    data.append(i)

with open("cx.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
